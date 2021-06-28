from typing import Dict
from flask_restful import Resource, request
from database.firestore import db, firestore


class ReversePayment(Resource):
    def post(self, baqala_id, subscriber_mobile):
        """
        route: "/reversePayment/<baqala_id>/<subscriber_mobile>"

        args:
            baqala_uid: The uid of the baqala making the request
            subscriber_mobile: The mobile number of the subscriber

        request json contains:
            reversed_timestamp: The timetsamp for the reversed timestamp

        output:
            creates new document in hisabHistory subcollection
                {
                    type: "hisab"
                    "amount": request_data["amount],
                    "before": current total hisab,
                    "after" current total hisab + "amount"
                    "timestamp": firestore.SERVER_TIMESTAMP,
                    # "payment_note": "reversal",
                    reversal_for: request_data["reversed_timestamp"]
                }
            updates hisab document with timestamp == request_data["reversed_timestamp"]
                {
                    is_reversed: True,
                    reversed_on: firestore.SERVER_TIMESTAMP
                }
            updates subscriber document
                {
                    "total_hisab": current total hisab + amount in the reversed document,
                    "last_payment": firestore.SERVER_TIMESTAMP
                }
        """
        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

        timestamp = firestore.SERVER_TIMESTAMP

        request_data: Dict = request.get_json()
        reversed_timestamp = request_data.get("reversed_timestamp")

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

        reversed_document_query = subscriber_hisab_history.where(
            "timestamp",
            "==",
            reversed_timestamp,
        )

        if not reversed_document_query:
            return {"Reversed document could not be found"}, 404

        reversed_document = reversed_document_query[0]

        reversed_amount = reversed_document.get("amount")
        current_total_hisab = subscriber_document.get("total_hisab")
        new_total_hisab = current_total_hisab - reversed_amount

        reversal_payment_dict = {
            # "type": "payment",
            "type": "reversal",
            "before": current_total_hisab,
            "after": new_total_hisab,
            "amount": reversed_amount,
            "timestamp": timestamp,
            # "payment_note": "reversal",
            "reversal_for": request_data["reversed_timestamp"],
        }

        wb = db.batch()

        # update subscriber document
        wb.update(
            subscriber_document_reference,
            {
                "total_hisab": new_total_hisab,
                "last_payment": timestamp,
            },
        )

        # update the reversed document
        wb.update(
            reversed_document.reference,
            {
                "is_reversed": True,
                "reversed_on": timestamp,
            },
        )

        # add new payment
        wb.set(
            subscriber_hisab_history.document(),
            reversal_payment_dict,
        )

        wb.commit()

        return {"message": "payment added successfully"}, 201
