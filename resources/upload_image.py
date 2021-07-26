from typing import Dict, List
from flask import json
from flask_restful import Resource, request
from database.firestore import db, firestore
from firebase_admin import storage


class UploadImage(Resource):
    def post(self):
        """
        request json:
            "baqala_id": ID of the baqala making the upload
            "images": Map of pairs of image title and image base64 data
        """
        request_data = request.get_json()
        baqala_id: str = request_data["baqala_id"]
        images: Dict[str, str] = request_data["images"]

        bucket = storage.bucket("hisab-android2.appspot.com")

        image_names = list(images.keys())
        image_bytes = list(images.values())

        for name, image in zip(image_names, image_bytes):
            blob = bucket.blob(f"{baqala_id}/{name}")
            blob.upload_from_string(image)

        # blob = bucket.blob(f"{baqala_id}/{image_names[0]}")
        # upload = blob.upload_from_string(image_bytes[0])

        # for a in dir(blob):
        #     print(a)

        return {"message": "upload succesfull"}, 200

        # ref = db.collection(baqala_id)
        # timestamp = firestore.SERVER_TIMESTAMP
