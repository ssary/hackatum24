from fastapi import APIRouter, HTTPException, Query
from src.domain.models.activity import ActivityModel
from src.application.services import activity_service
from src.infrastructure.database import activity_collection, user_collection
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/activity", tags=["Activity"])

@router.get("/available")
async def get_available_activities():
    current_time: datetime = datetime.utcnow()
    available_activities = []

    async for activity in activity_collection.find():
        end_time: datetime  = activity["timerange"]["endTime"]

        if (
            current_time < end_time and
            len(activity["joinedUsers"]) > 0 and
            len(activity["joinedUsers"]) < activity["maxUsers"]
        ):
            activity["id"] = str(activity["_id"])
            del activity["_id"]
            available_activities.append(activity)

    return available_activities

@router.post("/")
async def create_activity(activity: ActivityModel, created_by: str):
    # Check if the user exists
    if not await user_collection.find_one({"_id": created_by}):
        raise HTTPException(status_code=404, detail="User who created the activity not found")
    
    # Add the creator to the joinedUsers list
    activity_data = activity.dict()
    activity_data["joinedUsers"] = [created_by]  # Initialize joinedUsers with the creator's ID

    # Insert the activity into the database
    result = await activity_collection.insert_one(activity_data)
    return {"id": str(result.inserted_id)}

@router.get("/{activity_id}/similar")
async def get_top_k_similar_activities(
    activity_id: str, K: int = Query(5, description="Number of similar activities to return")
):
    """
    Get the top K similar activities to the specified activity.
    """
    similar_activities = await activity_service.get_top_K_similar_activities(activity_id, K)
    return similar_activities


@router.get("/{activity_id}")
async def get_activity(activity_id: str):
    activity = await activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Fetch user details for joinedUsers
    user_ids = activity.get("joinedUsers", [])
    users = []
    for user_id in user_ids:
        user = await user_collection.find_one({"_id": user_id})
        if user:
            user["id"] = str(user["_id"])
            del user["_id"]
            users.append(user)
    activity["joinedUsers"] = users

    activity["id"] = str(activity["_id"])
    del activity["_id"]
    return activity

@router.put("/{activity_id}/add_user/{user_id}")
async def add_user_to_activity(activity_id: str, user_id: str):
    # Check if activity exists
    activity = await activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if user exists
    user = await user_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Add user to joinedUsers if not already added
    if user_id not in activity.get("joinedUsers", []):
        await activity_collection.update_one(
            {"_id": ObjectId(activity_id)},
            {"$push": {"joinedUsers": user_id}}
        )
        return {"message": "User added to activity successfully"}
    else:
        return {"message": "User already in activity"}
    
@router.put("/{activity_id}/remove_user/{user_id}")
async def remove_user_from_activity(activity_id: str, user_id: str):
    # Check if the activity exists
    activity = await activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if the user exists in the joinedUsers list
    if user_id not in activity.get("joinedUsers", []):
        raise HTTPException(status_code=404, detail="User not part of the activity")
    
    # Remove the user from joinedUsers
    await activity_collection.update_one(
        {"_id": ObjectId(activity_id)},
        {"$pull": {"joinedUsers": user_id}}
    )

    return {"message": "User removed from activity successfully"}

@router.put("/{activity_id}")
async def update_activity(activity_id: str, activity: ActivityModel):
    updated_data = activity.dict(exclude_unset=True)
    result = await activity_collection.update_one(
        {"_id": ObjectId(activity_id)}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity updated successfully"}

@router.delete("/{activity_id}")
async def delete_activity(activity_id: str):
    result = await activity_collection.delete_one({"_id": ObjectId(activity_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}
