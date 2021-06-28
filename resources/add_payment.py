from typing import Dict
from flask_restful import Resource, request
from database.firestore import db, firestore


class AddPayment(Resource):
    def post(self, baqala_id, subscriber_mobile):
        """
        route: "/addPayment/<baqala_id>/<subscriber_mobile>"

        add a new payment to the subscriber with mobile = subscriber_mobile

        args:
            baqala_id: id of the baqala
            subscriber_mobile: mobile number of the subscriber

        request json:
            type: payment
            amount: amount of the new payment

        output:
            creates new document in hisabHistory subcollection
                {
                    "type": requset_data["type"]
                    "amount": "request_data["ammount],
                    "before": current total hisab,
                    "after" current total hisab + "amount"
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    # "payment_note": "normal",
                }

            updates subscriber document
                {
                    "total_hisab": current total hisab + request_data["amount"],
                    "last_hisab": firestore.SERVER_TIMESTAMP
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
        subscriber_hisab_history_reference = subscriber_document_reference.collection(
            "hisabHistory"
        )

        current_total_hisab = subscriber_document.get("total_hisab")
        new_total_hisab = current_total_hisab - request_data.get("amount")

        request_data["before"] = current_total_hisab
        request_data["after"] = new_total_hisab
        request_data["timestamp"] = timestamp
        # request_data["payment_note"] = "normal"

        wb = db.batch()

        wb.update(
            subscriber_document_reference,
            {
                "total_hisab": new_total_hisab,
                "last_payment": timestamp,
            },
        )

        wb.set(
            subscriber_hisab_history_reference.document(),
            request_data,
        )

        wb.commit()

        return {"message": "payment added successfully"}, 201
