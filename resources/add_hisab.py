from typing import Dict
from flask_restful import Resource, request
from database.firestore import db, firestore


class AddHisab(Resource):
    def post(self, baqala_id: str, subscriber_mobile: str):
        """
        route: "/addHisab/<baqala_id>/<subscriber_mobile>"

        add a new hisab to the subscriber with mobile = subscriber_mobile

        args:
            baqala_id: id of the baqala
            subscriber_mobile: mobile number of the subscriber

        request json:
            type: hisab
            amount: amount of the new hisab
        output:
            {
                "type": request_data["hisab"]
                "amount": "request_data["ammount],
                "before": current total hisab,
                "after" current total hisab + "amount",
                "timestamp": firestore.SERVER_TIMESTAMP,
                "is_reversed": False,
                "reversed_on: None,
            }
        """
        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

        timestamp = firestore.SERVER_TIMESTAMP

        request_data: Dict = request.get_json()

        subscriber_document_query = (
            db.collection(baqala_id).where("mobile", "==", subscriber_mobile).get()
        )

        if not subscriber_document_query:
            return {
                "message": f"Either baqala id is wrong, or a subscriber with the mobile number {subscriber_mobile} does not exist"
            }, 404  # not found

        subscriber_document = subscriber_document_query[0]
        subscriber_document_reference = subscriber_document.reference
        subscriber_hisab_history = subscriber_document_reference.collection(
            "hisabHistory"
        )

        current_total_hisab = subscriber_document.get("total_hisab")
        new_total_hisab = current_total_hisab + request_data.get("amount")

        request_data["before"] = current_total_hisab
        request_data["after"] = new_total_hisab
        request_data["timestamp"] = timestamp
        request_data["is_reversed"] = False
        request_data["reversed_on"] = None

        wb = db.batch()

        wb.update(
            subscriber_document_reference,
            {
                "total_hisab": new_total_hisab,
                "last_hisab": timestamp,
            },
        )

        wb.set(
            subscriber_hisab_history.document(),
            request_data,
        )

        wb.commit()

        return {"message": "hisab added successfully"}, 201
