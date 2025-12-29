import pandas as pd


def recommend_accident_plan():
    """
    Recommend the best personal accident insurance plan
    """

    # Load data
    plans_df = pd.read_csv("data/processed/accident_plans.csv")
    companies_df = pd.read_csv("data/processed/insurance_companies.csv")

    # Attach company final score
    plans_df = plans_df.merge(
        companies_df[["company", "company_score"]],
        on="company",
        how="inner"
    )

    # Rank plans
    plans_df = plans_df.sort_values(
        by=["company_score", "coverage_amount", "annual_cost"],
        ascending=[False, False, True]
    )

    best_plan = plans_df.iloc[0]

    return {
        "company": best_plan["company"],
        "plan_name": best_plan["plan_name"],
        "coverage_amount": int(best_plan["coverage_amount"]),
        "annual_cost": int(best_plan["annual_cost"])
    }
