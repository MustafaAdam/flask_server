from typing import Dict, List
from flask import json
from flask_restful import Resource, request
from database.firestore import db, firestore


class Baqala(Resource):
    def get(self, baqala_id):
        """
        "route": /<baqala_id>

        retrieves the list of subscribers in collection [baqala_id]

        output:
            Dict[str: List]: { "subscribers": [ <list of subscribers> ]}
        """
        result: List[Dict] = []
        baqala_ref = db.collection(baqala_id)
        subscribers: list[firestore.DocumentSnapshot] = baqala_ref.get()

        if not subscribers:
            return {
                "message": f"subscriber with this ID number {baqala_id} does nto exist"
            }, 404  # not found

        for subscriber in subscribers:
            name: str = subscriber.get("name")
            mobile: str = subscriber.get("mobile")
            total_hisab: float = subscriber.get("total_hisab")
            last_hisab: float = subscriber.get("last_hisab")
            last_payment: firestore.SERVER_TIMESTAMP = subscriber.get("last_payment")
            created_at: firestore.SERVER_TIMESTAMP = subscriber.get("created_at")

            result.append(
                {
                    "name": name,
                    "mobile": mobile,
                    "total_hisab": json.loads(json.dumps(total_hisab)),
                    "last_hisab": json.loads(json.dumps(last_hisab)),
                    "last_payment": json.loads(json.dumps(last_payment)),
                    "created_at": json.loads(json.dumps(created_at)),
                    # The timestamps are of type DateTimeWithNanoSeconds, which is not JSON Serializable.
                    # Without json.dumps, the timestamp will raise a TypeError
                    # The json.loads is to skip backslashes added beause of json.dumps()
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
                "message": f"Either baqala id is wrong, or a subscriber with the mobile number {subscriber_mobile} does not exist"
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
