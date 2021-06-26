from typing import List

from flask.json import jsonify
from utils import get_hisabs
from flask_restful import Resource
from database.firestore import db, firestore


class SubscriberHistory(Resource):
    def get(self, baqala_id, subscriber_mobile):

        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": "Subscriber mobile number is badly formatted (not digits only or length not 10)",
            }, 400  # bad request

        subscriber_document_query: list = (
            db.collection(baqala_id).where("mobile", "==", subscriber_mobile).get()
        )

        if not subscriber_document_query:
            return {
                "message": f"Subscriber with the mobile number {subscriber_mobile} does not exist"
            }, 404  # not found

        subscriber_document = subscriber_document_query[0]
        subscriber_document_reference = subscriber_document._reference

        hisab_history: List[firestore.DocumentSnapshot] = (
            subscriber_document_reference.collection("hisabHistory")
            .order_by("serverTimestamp", direction=firestore.Query.DESCENDING)
            .get()
        )

        hisabs = get_hisabs(hisab_history)

        return jsonify({"hisab history": hisabs})
