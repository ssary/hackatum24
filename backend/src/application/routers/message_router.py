from fastapi import APIRouter

router = APIRouter(prefix="/message", tags=["Message"])

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from src.domain.models.message import MessageModel
from src.infrastructure.database import activity_collection, user_collection

router = APIRouter(prefix="/message", tags=["Message"])


async def get_activity(activity_id: str):
    activity = await activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/{activity_id}")
async def get_messages(activity_id: str):
    activity = await get_activity(activity_id)
    if "messages" not in activity:
        activity["messages"] = []
    return activity["messages"]

@router.post("/{activity_id}")
async def create_message(activity_id: str, message: MessageModel, current_user_id: str):
    activity = await get_activity(activity_id)
    if current_user_id not in activity["joinedUsers"]:
        raise HTTPException(status_code=403, detail="Unauthorized to post message")

    if "messages" not in activity:
        activity["messages"] = []

    # Konvertiere das MessageModel in ein Dictionary
    activity["messages"].append(message.dict())

    await activity_collection.update_one(
        {"_id": ObjectId(activity_id)},
        {"$set": {"messages": activity["messages"]}}
    )
    return {"message": "Message created successfully"}


