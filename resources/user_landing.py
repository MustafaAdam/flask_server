from typing import List
from flask_restful import Resource
from database.firestore import db


class UserLanding(Resource):
    def get(self, user_id: str):
        # users_ref: List = db.collection("users").where("uid", "==", user_id).get()
        user_ref = db.collection("users").document(user_id).get()

        if not user_ref:
            return {"message": f"user with ID {user_id} was not found"}, 400

        user_document = user_ref.to_dict()

        if user_document.get("userType") == "baqala":
            return user_document, 200

        subscribed_to = user_document.get("subscribedTo")

        if subscribed_to:
            user_baqala_document = db.collection("users").document(subscribed_to).get()
            ab = {
                "user_document": user_document,
                "subscribed_to": user_baqala_document.to_dict(),
            }
            return ab, 200

        return user_document, 200
