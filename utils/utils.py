import datetime
from typing import Dict, List
from firebase_admin import firestore
from time import strptime, strftime


def get_hisabs(hisabs: List[firestore.DocumentSnapshot]) -> List[Dict]:
    """
    Returns a dictionary with all the hisabs fields and values

    Args:
        hisabs: list of the all hisabs

    Returns:
        dictionary that contains fields and values of the hisabs in Firestore

    """
    result = []

    for hisab in hisabs:
        hisab_dict: Dict = hisab.to_dict()

        hisab_type: str = hisab_dict.get("type", None)

        d = {}

        timestamp = hisab_dict.get("timestamp")

        proper_timestamp: str = get_proper_timestamp(timestamp.astimezone())

        d.update(
            {
                "hisab_type": hisab_dict.get("type", None),
                "timestamp": proper_timestamp,
                "amount": hisab_dict.get("amount", None),
                "before": hisab_dict.get("before", None),
                "after": hisab_dict.get("after", None),
            }
        )

        if hisab_type == "hisab":
            d["is_reversed"] = hisab_dict.get("is_reversed", False)
            d["reversed_on"] = hisab_dict.get("reversed_on", None)
        # elif hisab_type == "payment":
        #     # d["payment_note"] = hisab_dict.get("payment_note", None)
        #     # d["reversal_for"] = hisab_dict.get("reversal_for", None)
        #     pass
        elif hisab_type == "reversal":
            d["reversal_for"] = hisab_dict.get("reversal_for", None)
        result.append(d)

    return result


def get_methods_of_object(object_name):
    return [
        method_name
        for method_name in dir(object_name)
        if callable(getattr(object_name, method_name))
    ]


def get_proper_timestamp(timestamp) -> str:
    if not timestamp:
        return None

    date: datetime.date = timestamp.date()

    day = str(date.day)
    month = str(date.month)
    year = str(date.year)

    if len(month) == 1:
        month = f"0{month}"

    proper_date = f"{day} {month} {year}"

    weekday: int = date.weekday()
    proper_weekday: str = get_day_from_int(weekday)

    time = timestamp.time()
    hour = time.hour
    minute = time.minute
    temp = strptime(f"{hour}:{minute}", "%H:%M")

    proper_time: str = strftime("%I:%M %p", temp)

    return f"{proper_weekday}, {proper_date}.{proper_time}"


def get_day_from_int(integer: int) -> str:
    mapper = {
        0: "Mon",
        1: "Tues",
        2: "Wed",
        3: "Thur",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    return mapper[integer]
