from typing import Dict, List
from firebase_admin import firestore


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
        print(hisab_dict)

        hisab_type: str = hisab_dict.get("type", None)
        timestamp: firestore.SERVER_TIMESTAMP = hisab.get("serverTimestamp")
        amount: float = hisab_dict.get("amount", None)
        before: float = hisab_dict.get("before", None)
        after: float = hisab_dict.get("after", None)

        d = {}

        d.update(
            {
                "hisab_type": hisab_type,
                "timestamp": timestamp,
                "amount": amount,
                "before": before,
                "after": after,
            }
        )

        if hisab_type == "hisab":
            d["isCorrected"] = hisab_dict.get("isCorrected", None)
            d["correctedOn"] = hisab_dict.get("correctedOn", None)
        elif hisab_type == "payment":
            d["payment_note"] = hisab_dict.get("note", None)
            d["correctionFor"] = hisab_dict.get("correctedFor", None)

        result.append(d)

    return result
