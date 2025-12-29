import pandas as pd


# -----------------------------------
# Region keyword-based strength
# -----------------------------------
REGION_KEYWORDS = {
    "southeast": ["star", "care", "niva"],
    "southwest": ["star", "icici", "hdfc"],
    "northwest": ["hdfc", "icici", "bajaj"],
    "northeast": ["new india", "oriental", "national"]
}


def get_region_score(company: str, region: str) -> float:
    company_lower = company.lower()

    keywords = REGION_KEYWORDS.get(region, [])
    for kw in keywords:
        if kw in company_lower:
            return 0.2

    # pan-India PSU insurers get mild boost everywhere
    if any(psu in company_lower for psu in ["new india", "oriental", "national", "united"]):
        return 0.1

    return 0.0


def recommend_health_plan(user_age, children, predicted_premium, region):
    plans_df = pd.read_csv("data/processed/health_plans.csv")
    companies_df = pd.read_csv("data/processed/insurance_companies.csv")

    # Age-based filtering
    filtered_plans = plans_df[
        (plans_df["min_age"] <= user_age) &
        (plans_df["max_age"] >= user_age)
    ]

    if filtered_plans.empty:
        filtered_plans = plans_df.copy()

    # Merge company scores
    merged = filtered_plans.merge(
        companies_df,
        on="company",
        how="left"
    )

    # Apply region score
    merged["region_score"] = merged["company"].apply(
        lambda c: get_region_score(c, region)
    )

    # Final ranking
    merged["final_company_score"] = (
        merged["trust_score"]
        + merged["policy_score"]
        + merged["region_score"]
    )

    merged = merged.sort_values("final_company_score", ascending=False)

    best_plan = merged.iloc[0]

    return {
        "company": best_plan["company"],
        "plan_name": best_plan["plan_name"],
        "estimated_premium": int(predicted_premium)
    }
