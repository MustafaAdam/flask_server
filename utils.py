from typing import Dict, List
from firebase_admin import firestore
from flask import json


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

        x = hisab_dict.get("timestamp")

        print(get_methods_of_object(x))
        print(f"\n\n{type(x)}\n\n")
        print(x.hours)

        d.update(
            {
                "hisab_type": hisab_dict.get("type", None),
                "timestamp": json.loads(json.dumps(hisab_dict.get("timestamp", None))),
                "amount": hisab_dict.get("amount", None),
                "before": hisab_dict.get("before", None),
                "after": hisab_dict.get("after", None),
            }
        )

        if hisab_type == "hisab":
            d["is_reversed"] = hisab_dict.get("is_reversed", None)
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
