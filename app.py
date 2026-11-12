
import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Air Quality Prediction",
    page_icon="🌍",
    layout="wide"
)

with open("air_quality_model.pkl", "rb") as file:
    model = pickle.load(file)

with open("air_quality_accuracy.txt", "r") as file:
    accuracy = float(file.read())

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "result" not in st.session_state:
    st.session_state.result = None

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #d6eaff, #ffffff);
}
h1 {
    color: #123b63 !important;
    text-align: center;
}
h2, h3, h4, p, label {
    color: #123b63 !important;
}
.stButton button {
    background-color: #1769aa;
    color: white;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# WELCOME PAGE
if st.session_state.page == "welcome":

    st.title("🌍 Welcome!")

    st.markdown(
        "<h3 style='text-align:center;'>"
        "Machine Learning Based Air Quality Prediction System"
        "</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;'>"
        "Smart Air Pollution Monitoring & Prediction"
        "</h4>",
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?w=1000",
        use_container_width=True
    )

    st.info(
        "This system predicts air quality using "
        "machine learning and pollution parameters."
    )

    if st.button("Get Started 🌿", use_container_width=True):
        st.session_state.page = "prediction"
        st.rerun()

# PREDICTION PAGE
elif st.session_state.page == "prediction":

    st.title("🌍 Air Quality Prediction System")

    st.metric("Model Test Accuracy", f"{accuracy:.2f}%")

    st.info("Enter the air pollution values.")

    col1, col2, col3 = st.columns(3)

    with col1:
        pm25 = st.number_input("PM2.5", 0.0, 500.0, 15.0)
        pm10 = st.number_input("PM10", 0.0, 600.0, 25.0)

    with col2:
        no2 = st.number_input("NO2", 0.0, 300.0, 7.0)
        so2 = st.number_input("SO2", 0.0, 200.0, 5.0)

    with col3:
        co = st.number_input("CO", 0.0, 20.0, 0.5)
        o3 = st.number_input("O3", 0.0, 300.0, 25.0)

    if st.button("Predict Air Quality", key="predict_btn",
                 use_container_width=True):

        input_data = pd.DataFrame([{
            "PM2.5": pm25,
            "PM10": pm10,
            "NO2": no2,
            "SO2": so2,
            "CO": co,
            "O3": o3
        }])

        st.session_state.result = model.predict(input_data)[0]

    if st.session_state.result is not None:

        result = st.session_state.result
        st.subheader("Prediction Result")

        if result == "Good":
            st.success("Air Quality: GOOD 🌿")
        elif result == "Satisfactory":
            st.success("Air Quality: SATISFACTORY 😊")
        elif result == "Moderate":
            st.warning("Air Quality: MODERATE 🌤️")
        elif result == "Poor":
            st.error("Air Quality: POOR ⚠️")
        elif result == "Very Poor":
            st.error("Air Quality: VERY POOR 🚨")
        else:
            st.error("Air Quality: SEVERE ⚠️")

        if st.button("Finish & Thank You ❤️",
                     key="finish_btn",
                     use_container_width=True):
            st.session_state.page = "thankyou"
            st.rerun()

# THANK YOU PAGE
elif st.session_state.page == "thankyou":

    st.title("🙏 Thank You!")

    st.markdown(
        "<h3 style='text-align:center;'>"
        "Thank You for Using Our System!"
        "</h3>",
        unsafe_allow_html=True
    )

    st.success(
        "Your Air Quality Prediction has been completed successfully."
    )

    st.markdown(
        "<h4 style='text-align:center;'>"
        "Stay Safe 🌿 Breathe Clean Air 🌍"
        "</h4>",
        unsafe_allow_html=True
    )

    st.caption(
        "Developed using Python, Machine Learning and Streamlit."
    )

    if st.button("Back to Home 🏠", use_container_width=True):
        st.session_state.result = None
        st.session_state.page = "welcome"
        st.rerun()
