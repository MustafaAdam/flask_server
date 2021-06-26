from typing import Dict
from flask_restful import Resource, request
from database.firestore import db, firestore


class ReversePayment(Resource):
    def post(self, baqala_id, subscriber_mobile):
        """
        args:
            baqala_uid: The uid of the baqala making the request
            subscriber_mobile: The mobile number of the subscriber


        request json contains:
            reversedTimestamp: The timetsamp for the reversed timestamp
        """
        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

        timestamp = firestore.SERVER_TIMESTAMP

        request_data: Dict = request.get_json()
        reversed_timestamp = request_data.get("reversedTimestamp")

        subscriber_document_query = (
            db.collection(baqala_id).where("mobile", "==", subscriber_mobile).get()
        )

        if not subscriber_document_query:
            return {
                "message": "Subscriber with the mobile number {} does not exist".format(
                    subscriber_mobile
                )
            }, 404  # not found

        subscriber_document = subscriber_document_query[0]
        subscriber_document_reference = subscriber_document._reference
        subscriber_hisab_history = subscriber_document_reference.collection(
            "hisabHistory"
        )

        reversed_document_query = subscriber_hisab_history.where(
            "serverTimestamp",
            "==",
            reversed_timestamp,
        )

        if not reversed_document_query:
            return {"Reversed document could not be found"}, 404

        reversed_document = reversed_document_query[0]

        reversed_amount = reversed_document.get("amount")
        current_total_hisab = subscriber_document.get("totalHisab")
        new_total_hisab = current_total_hisab - reversed_amount

        reversal_payment_dict = {
            "before": current_total_hisab,
            "after": new_total_hisab,
            "amount": reversed_amount,
            "serverTimestamp": timestamp,
            "note": "reversal",
        }

        wb = db.batch()

        # update subscriber document
        wb.update(
            subscriber_document_reference,
            {
                "totalHisab": new_total_hisab,
                "lastPayment": timestamp,
            },
        )

        # update the reversed document
        wb.update(
            reversed_document._reference,
            {
                "isReversed": True,
                "reversedOn": timestamp,
            },
        )

        # add new payment
        wb.set(
            subscriber_hisab_history.document(),
            reversal_payment_dict,
        )

        wb.commit()

        return {"message": "payment added successfully"}, 201
