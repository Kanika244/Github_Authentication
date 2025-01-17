from motor.motor_asyncio import AsyncIOMotorClient
Mongo_url = "mongodb://127.0.0.1:27017"

client = AsyncIOMotorClient(Mongo_url)

database = client.get_database("social_auth")
collection = database.get_collection("users")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "login": user["login"],
        "email": user.get("email"),
        "avatar_url": user["avatar_url"],
        "html_url": user["html_url"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }