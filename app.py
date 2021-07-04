from resources.user_landing import UserLanding
from resources.clear_hisab import ClearSubscriberHisab
from resources.reverse_payment import ReversePayment
from resources.add_payment import AddPayment
from resources.add_hisab import AddHisab
from resources.subscriber_history import SubscriberHistory
from resources.baqala_subscriber import BaqalaSubscriber, BaqalaCount
from resources.users import Users
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

api = Api(app)

api.add_resource(Users, "/users")
api.add_resource(BaqalaSubscriber, "/<baqala_id>")
api.add_resource(BaqalaCount, "/count/<baqala_id>")
api.add_resource(SubscriberHistory, "/hisabHistory/<baqala_id>/<subscriber_mobile>")
api.add_resource(AddHisab, "/addHisab/<baqala_id>/<subscriber_mobile>")
api.add_resource(AddPayment, "/addPayment/<baqala_id>/<subscriber_mobile>")
api.add_resource(ReversePayment, "/reversePayment/<baqala_id>/<subscriber_mobile>")
api.add_resource(ClearSubscriberHisab, "/clearHisab/<baqala_id>/<subscriber_mobile>")
api.add_resource(UserLanding, "/users/<user_id>")

if __name__ == "__main__":
    app.run(debug=True)
