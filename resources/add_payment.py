from typing import Dict
from flask_restful import Resource, request
from database.firestore import db, firestore


class AddPayment(Resource):
    def post(self, baqala_id, subscriber_mobile):
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
                "message": f"Subscriber with the mobile number {subscriber_mobile} does not exist"
            }, 404  # not found

        subscriber_document = subscriber_document_query[0]
        subscriber_document_reference = subscriber_document._reference
        subscriber_hisab_history_reference = subscriber_document_reference.collection(
            "hisabHistory"
        )

        current_total_hisab = subscriber_document.get("totalHisab")
        new_total_hisab = current_total_hisab - request_data.get("amount")

        request_data["before"] = current_total_hisab
        request_data["after"] = new_total_hisab
        request_data["serverTimestamp"] = timestamp
        request_data["note"] = "normal"

        wb = db.batch()

        wb.update(
            subscriber_document_reference,
            {
                "totalHisab": new_total_hisab,
                "lastPayment": timestamp,
            },
        )

        wb.set(
            subscriber_hisab_history_reference.document(),
            request_data,
        )

        wb.commit()

        return {"message": "payment added successfully"}, 201
