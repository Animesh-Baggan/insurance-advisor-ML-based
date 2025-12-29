def recommend_travel_plan(trip_type, trip_days):
    if trip_type == "domestic":
        if trip_days <= 7:
            cost = 500
        elif trip_days <= 15:
            cost = 900
        elif trip_days <= 30:
            cost = 1500
        else:
            return None

        return {
            "company": "HDFC ERGO General Insurance",
            "plan_name": "Domestic Travel Secure",
            "estimated_cost": cost
        }

    if trip_type == "international":
        if trip_days <= 7:
            cost = 2000
        elif trip_days <= 15:
            cost = 3500
        elif trip_days <= 30:
            cost = 6000
        else:
            return None

        return {
            "company": "Tata AIG General Insurance",
            "plan_name": "International Travel Guard",
            "estimated_cost": cost
        }

    return None
