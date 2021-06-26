from typing import Dict


class PersonalUser:
    def __init__(self, userInfo: Dict):
        self.uid = userInfo.get("uid", None)
        self.username = userInfo.get("username", None)
        self.email = userInfo.get("email", None)
        self.mobile = userInfo.get("mobile", None)
        self.subscribedTo = userInfo.get("subscribedTo", None)
        self.gender = userInfo.get("gender", None)
        self.userType = userInfo.get("userType", None)


class BaqalaUser:
    def __init__(self, baqalaInfo: Dict):
        self.uid = baqalaInfo.get("uid", None)
        self.username = baqalaInfo.get("username", None)
        self.userType = baqalaInfo.get("userType", None)
        self.email = baqalaInfo.get("email", None)
        self.mobile = baqalaInfo.get("mobile", None)
        self.landline = baqalaInfo.get("landline", None)
        self.lat = baqalaInfo.get("lat", None)
        self.long = baqalaInfo.get("long", None)
        self.opening = baqalaInfo.get("opening", None)
        self.closing = baqalaInfo.get("closing", None)
