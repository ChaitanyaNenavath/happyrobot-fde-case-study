def negotiate_rate(load_rate: float, carrier_offer: float):
    """
    Basic negotiation logic.
    Accepts carrier offers up to 10% above the loadboard rate.
    """

    if carrier_offer <= load_rate:
        return {
            "decision": "ACCEPT",
            "accepted": True,
            "final_rate": carrier_offer,
            "message": "Carrier offer accepted."
        }

    max_acceptable_rate = round(load_rate * 1.10, 2)

    if carrier_offer <= max_acceptable_rate:
        return {
            "decision": "ACCEPT",
            "accepted": True,
            "final_rate": carrier_offer,
            "message": "Counteroffer accepted within allowed range."
        }

    return {
        "decision": "COUNTER",
        "accepted": False,
        "counter_offer": max_acceptable_rate,
        "message": f"Carrier offer is too high. Counter at ${max_acceptable_rate}."
    }