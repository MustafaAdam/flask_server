from flask_restful import Resource
from database.firestore import db


class ClearSubscriberHisab(Resource):
    def delete(self, baqala_id, subscriber_mobile):
        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

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

        subscriber_document_reference.update(
            {"total_hisab": 0.0, "last_payment": None, "last_hisab": None}
        )

        for document in subscriber_hisab_history_reference.get():
            document.reference.delete()

        return (
            {"message": f"User {subscriber_mobile} had his hisab history cleared!"},
        )
