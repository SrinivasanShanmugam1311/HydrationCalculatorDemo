import streamlit as st

st.set_page_config(page_title="Hydration Calculator", page_icon="💧", layout="centered")
st.title("💧 Simple Hydration Calculator")

with st.form("hydration_form"):
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, step=0.5)
        activity_min = st.number_input("Active minutes today", min_value=0, value=30, step=5)
    with col2:
        climate = st.selectbox("Climate", ["Normal", "Hot", "Cold"], index=0)
        age_group = st.selectbox("Age group", ["Adult (18–60)", "Senior (60+)"], index=0)

    submitted = st.form_submit_button("Calculate")

def recommend_water_liters(weight_kg: float, activity_min: int, climate: str, age_group: str) -> dict:
    # Base: ~35 ml/kg (adults), ~30 ml/kg (seniors). Convert to liters.
    base_ml_per_kg = 35 if "Adult" in age_group else 30
    base_l = (base_ml_per_kg * weight_kg) / 1000.0

    # Activity: add ~350 ml per 30 min moderate activity
    activity_l = 0.35 * (activity_min / 30)

    # Climate adjustment
    climate_bonus = {"Normal": 0.0, "Hot": 0.75, "Cold": 0.0}[climate]

    total = round(base_l + activity_l + climate_bonus, 2)
    return {
        "base_l": round(base_l, 2),
        "activity_l": round(activity_l, 2),
        "climate_l": round(climate_bonus, 2),
        "total_l": total,
    }

if submitted:
    rec = recommend_water_liters(weight, activity_min, climate, age_group)
    st.metric("Recommended water (L/day)", rec["total_l"])
    with st.expander("Breakdown"):
        st.write(f"• Base: **{rec['base_l']} L**")
        st.write(f"• Activity: **{rec['activity_l']} L**")
        st.write(f"• Climate: **{rec['climate_l']} L**")
    st.caption("Tip: Spread intake across the day. Adjust for medical conditions as advised by your doctor.")
