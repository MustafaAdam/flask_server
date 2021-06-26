from resources.reverse_payment import ReversePayment
from resources.add_payment import AddPayment
from resources.add_hisab import AddHisab
from resources.subscriber_history import SubscriberHistory
from resources.baqala import Baqala, BaqalaCount
from resources.users import Users
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

api = Api(app)

api.add_resource(Users, "/users")
api.add_resource(Baqala, "/<baqala_id>")
api.add_resource(BaqalaCount, "/<baqala_id>/count")
api.add_resource(SubscriberHistory, "/hisabHistory/<baqala_id>/<subscriber_mobile>")
api.add_resource(AddHisab, "/addHisab/<baqala_id>/<subscriber_mobile>")
api.add_resource(AddPayment, "/addPayment/<baqala_id>/<subscriber_mobile>")
api.add_resource(ReversePayment, "/reversePayment/<baqala_id>/<subscriber_mobile>")


if __name__ == "__main__":
    app.run(debug=True)
