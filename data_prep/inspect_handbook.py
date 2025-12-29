import pandas as pd

file_path = "data/raw/HandBook_Health_Insurance.xlsx"

# ---------- SHEET 66: CLAIMS / TRUST ----------
claims_df = pd.read_excel(file_path, sheet_name="66", skiprows=3)

claims_df = claims_df[["Unnamed: 1", "Unnamed: 136"]]
claims_df.columns = ["company", "incurred_claim_ratio"]

claims_df = claims_df.dropna(subset=["company", "incurred_claim_ratio"])
claims_df = claims_df[
    ~claims_df["company"].str.contains("Total|Sector|Insurers", case=False, na=False)
]

claims_df["incurred_claim_ratio"] = pd.to_numeric(claims_df["incurred_claim_ratio"])

# Normalize claim ratio (lower is better)
max_ratio = claims_df["incurred_claim_ratio"].max()
min_ratio = claims_df["incurred_claim_ratio"].min()

claims_df["trust_score"] = 1 - (
    (claims_df["incurred_claim_ratio"] - min_ratio)
    / (max_ratio - min_ratio)
)

claims_df = claims_df[["company", "trust_score"]]

# ---------- SHEET 62: POLICY VOLUME ----------
policy_df = pd.read_excel(file_path, sheet_name="62", skiprows=3)

policy_df = policy_df[["Unnamed: 1", "TOTAL.8"]]
policy_df.columns = ["company", "total_policies"]

policy_df = policy_df.dropna(subset=["company", "total_policies"])
policy_df = policy_df[
    ~policy_df["company"].str.contains("Total|Sector|Insurers", case=False, na=False)
]

policy_df["total_policies"] = pd.to_numeric(policy_df["total_policies"])

# Normalize policy volume (higher is better)
max_policies = policy_df["total_policies"].max()
min_policies = policy_df["total_policies"].min()

policy_df["policy_score"] = (
    (policy_df["total_policies"] - min_policies)
    / (max_policies - min_policies)
)

policy_df = policy_df[["company", "policy_score"]]

# ---------- FINAL MERGE ----------
final_df = claims_df.merge(policy_df, on="company", how="inner")

# ---------- FINAL COMPANY SCORE ----------
final_df["company_score"] = (
    0.6 * final_df["trust_score"] +
    0.4 * final_df["policy_score"]
)

# Sort by best insurers
final_df = final_df.sort_values("company_score", ascending=False)

print("Final insurer ranking:")
print(final_df.head(10))

# ---------- SAVE FINAL DATASET ----------
output_path = "data/processed/insurance_companies.csv"
final_df.to_csv(output_path, index=False)

print(f"\nFinal dataset saved to: {output_path}")