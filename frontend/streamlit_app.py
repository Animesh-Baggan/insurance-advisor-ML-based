# =====================================================
# PATH FIX
# =====================================================
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# =====================================================
# IMPORTS
# =====================================================
import streamlit as st
import requests
from datetime import datetime

from logic.recommend_health_plan import recommend_health_plan
from logic.recommend_travel_plan import recommend_travel_plan
from logic.recommend_accident_plan import recommend_accident_plan

# =====================================================
# CONFIG
# =====================================================
API_URL = "http://127.0.0.1:8001/predict"

st.set_page_config(
    page_title="Smart Insurance Advisor",
    page_icon="🛡️",
    layout="centered"
)

# =====================================================
# UI BEAUTIFICATION (CSS ONLY — NO LOGIC CHANGE)
# =====================================================
st.markdown(
    """
    <style>
    /* -------- APP BACKGROUND -------- */
    .stApp {
        background: linear-gradient(135deg, #1e1e1e, #2b2b2b);
        color: #f2f2f2;
    }

    /* -------- GLOBAL CARD STYLE -------- */
    div[data-testid="stContainer"] {
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 22px;
        box-shadow: 0px 12px 28px rgba(0,0,0,0.45);
    }

    /* -------- HEADINGS -------- */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700;
    }

    /* -------- TEXT -------- */
    label, p, .stMarkdown {
        color: #e0e0e0 !important;
        font-size: 15px;
    }

    /* -------- METRICS -------- */
    div[data-testid="metric-container"] {
        background-color: rgba(255,255,255,0.08);
        padding: 14px;
        border-radius: 12px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.4);
    }

    /* -------- INPUTS -------- */
    input, select, textarea {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #555 !important;
    }

    /* -------- BUTTONS -------- */
    button[kind="primary"] {
        background: linear-gradient(135deg, #3a7bd5, #3a6073);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
    }

    button[kind="primary"]:hover {
        transform: scale(1.02);
        opacity: 0.95;
    }

    /* -------- DOWNLOAD BUTTON -------- */
    .stDownloadButton button {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: #000;
        font-weight: 700;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# =====================================================
# HEADER
# =====================================================
st.title("🛡️ Smart Insurance Advisor")
st.caption("Health insurance first. Add-ons optional. Clear final cost.")
st.divider()

# =====================================================
# SECTION 1 — HEALTH INSURANCE
# =====================================================
with st.container(border=True):
    st.subheader("1️⃣ Health Insurance Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 18, 100, 30)
        bmi = st.number_input("BMI", 10.0, 50.0, 25.4)
        children = st.slider("Number of Children", 0, 5, 1)

    with col2:
        sex = st.selectbox("Sex", ["male", "female"])
        smoker = st.selectbox("Smoker", ["yes", "no"])
        region = st.selectbox(
            "Region",
            ["northwest", "northeast", "southeast", "southwest"]
        )

    if st.button("🔮 Predict Health Insurance"):
        payload = {
            "age": age,
            "sex": sex,
            "bmi": bmi,
            "children": children,
            "smoker": smoker,
            "region": region
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                st.session_state.prediction_result = response.json()
                st.session_state.predicted = True
            else:
                st.error("Prediction API error")
        except Exception as e:
            st.error(f"API connection failed: {e}")

    if st.session_state.predicted:
        predicted_premium = int(
            st.session_state.prediction_result["predicted_premium"]
        )

        health_plan = recommend_health_plan(
            user_age=age,
            children=children,
            predicted_premium=predicted_premium,
            region=region
        )

        st.success("✅ Health Insurance Recommendation")

        st.metric(
            "Estimated Annual Premium",
            f"₹ {predicted_premium:,.0f}"
        )

        st.markdown(
            f"""
**Company:** {health_plan['company']}  
**Plan:** {health_plan['plan_name']}
"""
        )

# =====================================================
# SECTION 2 — ADD-ONS
# =====================================================
if st.session_state.predicted:
    st.divider()

    with st.container(border=True):
        st.subheader("2️⃣ Optional Add-On Insurance")

        col1, col2 = st.columns(2)

        travel_plan = None
        accident_plan = None
        trip_type = None
        trip_days = None

        with col1:
            with st.container(border=True):
                st.subheader("✈️ Travel Insurance")

                add_travel = st.checkbox("Add Travel Insurance")

                if add_travel:
                    trip_type = st.radio(
                        "Trip Type",
                        ["domestic", "international"],
                        horizontal=True
                    )
                    trip_days = st.slider("Trip Duration (days)", 1, 60, 7)

                    travel_plan = recommend_travel_plan(trip_type, trip_days)

                    if travel_plan:
                        st.markdown(
                            f"""
**Company:** {travel_plan['company']}  
**Plan:** {travel_plan['plan_name']}  
**Cost:** ₹ {travel_plan['estimated_cost']:,.0f}
"""
                        )
                    else:
                        st.warning("No travel plan available")

        with col2:
            with st.container(border=True):
                st.subheader("🛡️ Accident Insurance")

                add_accident = st.checkbox("Add Accident Insurance")

                if add_accident:
                    accident_plan = recommend_accident_plan()

                    st.markdown(
                        f"""
**Company:** {accident_plan['company']}  
**Coverage:** ₹ {accident_plan['coverage_amount']:,.0f}  
**Cost:** ₹ {accident_plan['annual_cost']:,.0f}
"""
                    )

# =====================================================
# SECTION 3 — FINAL PACKAGE + DOWNLOAD
# =====================================================
if st.session_state.predicted:
    st.divider()

    total_cost = predicted_premium
    if travel_plan:
        total_cost += travel_plan["estimated_cost"]
    if accident_plan:
        total_cost += accident_plan["annual_cost"]

    monthly_total = total_cost / 12
    generated_on = datetime.now().strftime("%d %b %Y, %I:%M %p")

    with st.container(border=True):
        st.subheader("3️⃣ Full Package Details")

        st.metric("TOTAL ANNUAL PAYABLE", f"₹ {total_cost:,.0f}")
        st.metric("Approx. Monthly Cost", f"₹ {monthly_total:,.0f}")

        # RECEIPT LOGIC (UNCHANGED)
        summary_text = f"""
========================================
        INSURANCE SUMMARY RECEIPT
========================================

Generated On : {generated_on}
...
"""

        st.download_button(
            "📄 Download Insurance Receipt",
            summary_text,
            file_name="insurance_summary_receipt.txt",
            mime="text/plain"
        )

        if st.button("🔄 Start New Prediction"):
            st.session_state.predicted = False
            st.session_state.prediction_result = None
            st.rerun()
