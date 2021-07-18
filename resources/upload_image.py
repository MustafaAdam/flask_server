from typing import Dict, List
from flask import json
from flask_restful import Resource, request
from database.firestore import db, firestore
from firebase_admin import storage


class UploadImage(Resource):
    def post(self):
        request_data: Dict = request.get_json()
        baqala_id = request_data.get("baqalaID")
        imageBytes = request_data.get("imageBytes")

        print(f"baqala ID: {baqala_id}")
        print(f"Image bytes: {imageBytes}")

        bucket = storage.bucket("hisab-android2.appspot.com")

        # for a in dir(bucket):
        #     print(a)

        blob = bucket.blob(f"{baqala_id}/{imageBytes}")

        # print(blob._dict__)
        # for a in dir(blob):
        #     print(a)
        upload = blob.upload_from_string(imageBytes)
        print(upload)

        return {"message": "upload succesfull"}, 200

        # ref = db.collection(baqala_id)
        # timestamp = firestore.SERVER_TIMESTAMP
