from fastapi import APIRouter, HTTPException, Depends
from src.domain.models.user import UserModel
from src.infrastructure.database import user_collection

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/")
async def create_user(user: UserModel):
    if not user.userId:
        raise ValueError("User ID is required for user creation.")

    user_data = user.model_dump()
    user_data["_id"] = user.userId # userId === deviceId from flutter!!!!
    result = await user_collection.insert_one(user_data)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await user_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return user

@router.put("/{user_id}")
async def update_user(user_id: str, user: UserModel):
    updated_data = user.dict(exclude_unset=True)
    result = await user_collection.update_one(
        {"_id": user_id}, {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await user_collection.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
