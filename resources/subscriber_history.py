from typing import List
from utils.utils import get_hisabs
from flask_restful import Resource
from database.firestore import db, firestore


class SubscriberHistory(Resource):
    """
    route: "/hisabHistory/<baqala_id>/<subscriber_mobile>

    retrives the hisab history of subscriber with mobile = subscriber_mobile
    """

    def get(self, baqala_id, subscriber_mobile):

        if len(subscriber_mobile) != 10 or not subscriber_mobile.isdigit():
            return {
                "message": f"Either baqala id is wrong, or a subscriber with the mobile number {subscriber_mobile} does not exist"
            }, 400  # bad request

        subscriber_document_query: list = (
            db.collection(baqala_id).where("mobile", "==", subscriber_mobile).get()
        )

        if not subscriber_document_query:
            return {
                "message": f"Either baqala id is wrong, or a subscriber with the mobile number {subscriber_mobile} does not exist"
            }, 404  # not found

        subscriber_document = subscriber_document_query[0]
        subscriber_document_reference = subscriber_document.reference

        hisab_history: List[firestore.DocumentSnapshot] = (
            subscriber_document_reference.collection("hisabHistory")
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .get()
        )

        hisabs = get_hisabs(hisab_history)

        if not hisabs:
            return {
                "message": "This user does not have a hisab history"
            }, 204  # No content

        return hisabs, 200
