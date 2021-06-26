from flask.json import jsonify
from flask_restful import Resource
from database.firestore import db, firestore


class Baqala(Resource):
    def get(self, baqala_id):
        result = []
        baqala_ref = db.collection(baqala_id)
        subscribers: list[firestore.DocumentSnapshot] = baqala_ref.get()

        if not subscribers:
            return {
                "message": f"subscriber with this ID number {baqala_id} does nto exist"
            }, 404  # not found

        for subscriber in subscribers:
            name: str = subscriber.get("name")
            mobile: str = subscriber.get("mobile")
            totalHisab: float = subscriber.get("totalHisab")
            lastPayment: firestore.SERVER_TIMESTAMP = subscriber.get("lastPayment")
            createdAt: firestore.SERVER_TIMESTAMP = subscriber.get("createdAt")

            result.append(
                {
                    "name": name,
                    "mobile": mobile,
                    "totalHisab": totalHisab,
                    "lastPayment": lastPayment,
                    "createdAt": createdAt,
                }
            )

        return jsonify({"subscribers": result})


class BaqalaCount(Resource):
    def get(self, baqala_id):
        baqala_ref = db.collection(baqala_id)
        subscribers: list[firestore.DocumentSnapshot] = baqala_ref.get()

        if not subscribers:
            return {
                "message": "subscriber with this ID number {} does nto exist".format(
                    baqala_id
                )
            }, 404  # not found

        return {"subscriber count": len(subscribers)}
