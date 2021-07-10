from typing import Dict, List
from flask import json
from flask_restful import Resource, request
from database.firestore import db, firestore
from utils.utils import get_proper_timestamp


class BaqalaSubscriber(Resource):
    def get(self, baqala_id):
        """
        "route": /<baqala_id>

        retrieves the list of subscribers in collection [baqala_id]

        output:
            Dict[str: List]: { "subscribers": [ <list of subscribers> ]}
        """
        result: List[Dict] = []
        baqala_ref = db.collection(baqala_id)
        subscribers: list[firestore.DocumentSnapshot] = baqala_ref.order_by(
            "total_hisab", direction=firestore.Query.DESCENDING
        ).get()

        print(subscribers)

        if not subscribers:
            return {
                "message": f"baqala with this ID number {baqala_id} does not exist"
            }, 404  # not found

        for subscriber in subscribers:
            xx = subscriber.to_dict()

            name: str = subscriber.get("name")
            mobile: str = subscriber.get("mobile")
            total_hisab: float = subscriber.get("total_hisab")
            last_hisab: firestore.SERVER_TIMESTAMP = subscriber.get("last_hisab")
            last_payment: firestore.SERVER_TIMESTAMP = subscriber.get("last_payment")
            created_at: firestore.SERVER_TIMESTAMP = subscriber.get("created_at")

            result.append(
                {
                    "name": name,
                    "mobile": mobile,
                    "total_hisab": total_hisab,
                    "last_hisab": get_proper_timestamp(last_hisab),
                    "last_payment": get_proper_timestamp(last_payment),
                    "created_at": get_proper_timestamp(created_at),
                }
            )

        return result, 200

    def post(self, baqala_id):
        """
        "route": /<baqala_id>

        creates a new subscriber under this baqala account

        args:
            baqala_id: user id of the baqala

        request json has:
            "name": username of the subscriber
            "mobile": subscriber's mobile
            "total_hisab": The total previous hisab amount if any

        output:
            creates new document in baqala_id collection
                {
                    "name": request_data["name"],
                    "mobile": request_data["mobile"]
                    "total_hisab": request_data["total_hisab"]
                    "created_at" = firestore.SERVER_TIMESTAMP
                    "last_hisab" = None
                    "last_payment" = None
                }
            creates new document in hisabHistory subcollection
                {
                    "type": "hisab"
                    "before": 0.0,
                    "amount": request_data["total_hisab"],
                    "after": request_data["total_hisab"],
                    "timestamp": timestamp,
                    "is_reversed": False,
                    "reversed_on": None,
                },
        """

        timestamp = firestore.SERVER_TIMESTAMP

        request_data: Dict = request.get_json()

        subscriber_mobile = request_data["mobile"]

        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

        subscriber_document_query = (
            db.collection(baqala_id).where("mobile", "==", subscriber_mobile).get()
        )

        if subscriber_document_query:
            return {
                "message": f"duplicate mobile number"
            }, 400  # bad request: duplicate mobile number

        request_data["created_at"] = timestamp
        request_data["last_hisab"] = None
        request_data["last_payment"] = None

        new_subscriber_document = db.collection(baqala_id).document()

        wb = db.batch()

        wb.set(new_subscriber_document, request_data)

        wb.set(
            new_subscriber_document.collection("hisabHistory").document(),
            {
                "type": "hisab",
                "before": 0.0,
                "amount": request_data["total_hisab"],
                "after": request_data["total_hisab"],
                "timestamp": timestamp,
                "is_reversed": False,
                "reversed_on": None,
            },
        )

        wb.commit()

        return {"Success": "Subscriber created successfully"}, 201


class BaqalaCount(Resource):
    def get(self, baqala_id):
        baqala_ref = db.collection(baqala_id)
        subscribers: list[firestore.DocumentSnapshot] = baqala_ref.get()

        if not subscribers:
            return {
                "message": f"subscriber with this ID number {baqala_id} does nto exist"
            }, 404  # not found

        return {"subscriber count": len(subscribers)}
