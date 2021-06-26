from typing import Dict
from models.user import BaqalaUser, PersonalUser
from flask_restful import Resource
from database.firestore import db

users_ref = db.collection("users")


class Users(Resource):
    def get(self):
        users = {"personalUsers": [], "baqalaUsers": []}

        for userDocument in users_ref.get():
            userDict: Dict = userDocument.to_dict()
            userType = userDict.get("userType")
            if userType == "user":
                user = PersonalUser(userInfo=userDict)
                users["personalUsers"].append(user.__dict__)
            else:
                user = BaqalaUser(baqalaInfo=userDict)
                users["baqalaUsers"].append(user.__dict__)

        users["baqalaUsersCount"] = len(users["baqalaUsers"])
        users["personalUsersCount"] = len(users["personalUsers"])

        return {"users": users}
