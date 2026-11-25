
import streamlit as st
import pandas as pd
import numpy as np
import json
import sqlite3
from pathlib import Path
# ---------------- LOAD INDIAN HOUSE DATASET ----------------

property_data = pd.read_csv("dataset/indian_house_prices.csv")

cities = sorted(property_data["City"].dropna().unique())

property_types = sorted(
    property_data["Property_Type"].dropna().unique()
)

furnishing_options = sorted(
    property_data["Furnishing_Status"].dropna().unique()
)
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "house_price_model.json"
DATASET_PATH = BASE_DIR / "dataset" / "house_data.csv"
DATABASE_PATH = BASE_DIR / "estateiq.db"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="EstateIQ | AI Property Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111c30;
    border-right: 1px solid #263650;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label, span {
    color: #cbd5e1;
}

.hero {
    background: linear-gradient(120deg, #172b4d, #123b50);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #31516e;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    margin-bottom: 5px;
}

.hero p {
    color: #b8cce0;
    font-size: 16px;
}

.metric-card {
    background: #142238;
    border: 1px solid #2b405d;
    padding: 20px;
    border-radius: 15px;
    min-height: 115px;
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
}

.metric-value {
    color: #f8fafc;
    font-size: 25px;
    font-weight: 700;
    margin-top: 8px;
}

.section-card {
    background: #142238;
    border: 1px solid #2b405d;
    padding: 22px;
    border-radius: 15px;
    margin-bottom: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #0d9488, #0891b2);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 700;
    width: 100%;
}

div.stButton > button:hover {
    background: #0f766e;
    color: white;
    border: none;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 25px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

try:
    with MODEL_PATH.open("r", encoding="utf-8") as file:
        model = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as error:
    st.error(f"House price model could not be loaded: {error}")
    st.stop()

# ---------------- LOAD INDIAN HOUSE MODEL ----------------

try:
    with (BASE_DIR / "models" / "indian_house_model.json").open(
        "r",
        encoding="utf-8"
    ) as file:
        indian_model = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    indian_model = None


# ---------------- DATABASE MANAGEMENT ----------------

def initialize_database():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            area REAL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            age INTEGER,
            predicted_price REAL,
            price_per_sqft REAL
        )
    """)
    
    connection.execute("""
        CREATE TABLE IF NOT EXISTS indian_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            city TEXT,
            locality TEXT,
            property_type TEXT,
            bhk INTEGER,
            size_sqft REAL,
            property_age INTEGER,
            furnishing TEXT,
            parking INTEGER,
            metro_distance REAL,
            school_distance REAL,
            hospital_distance REAL,
            location_rating INTEGER,
            amenities_score INTEGER,
            predicted_price REAL
        )
    """)


    connection.commit()
    connection.close()


def save_prediction(record):

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT INTO predictions
        (date, area, bedrooms, bathrooms, age,
         predicted_price, price_per_sqft)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        record["Date"],
        record["Area"],
        record["Bedrooms"],
        record["Bathrooms"],
        record["Age"],
        record["Predicted Price"],
        record["Price per Sq Ft"]
    ))

    connection.commit()
    connection.close()


def get_prediction_history():

    connection = sqlite3.connect(DATABASE_PATH)

    history = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        connection
    )

    connection.close()

    return history


def clear_prediction_history():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("DELETE FROM predictions")

    connection.commit()
    connection.close()

# ---------------- INDIAN PREDICTION HISTORY ----------------

def save_indian_prediction(record):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("""
        INSERT INTO indian_predictions (
            date, city, locality, property_type, bhk,
            size_sqft, property_age, furnishing, parking,
            metro_distance, school_distance, hospital_distance,
            location_rating, amenities_score, predicted_price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["date"],
        record["city"],
        record["locality"],
        record["property_type"],
        record["bhk"],
        record["size_sqft"],
        record["property_age"],
        record["furnishing"],
        record["parking"],
        record["metro_distance"],
        record["school_distance"],
        record["hospital_distance"],
        record["location_rating"],
        record["amenities_score"],
        record["predicted_price"]
    ))

    connection.commit()
    connection.close()


def get_indian_prediction_history():
    connection = sqlite3.connect(DATABASE_PATH)

    history = pd.read_sql_query(
        "SELECT * FROM indian_predictions ORDER BY id DESC",
        connection
    )

    connection.close()
    return history


def clear_indian_prediction_history():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("DELETE FROM indian_predictions")
    connection.commit()
    connection.close()
# Initialize database
initialize_database()

# ---------------- PREDICTION HISTORY ----------------

if "prediction_history" not in st.session_state:
    st.session_state["prediction_history"] = []

# ---------------- HELPER FUNCTION ----------------

def predict_price(area, bedrooms, bathrooms, age):
    features = np.array([area, bedrooms, bathrooms, age], dtype=float)
    coefficients = np.array(model["coefficients"], dtype=float)

    prediction = model["intercept"] + np.dot(features, coefficients)
    return max(0.0, float(prediction))


def predict_indian_price(
    city,
    locality,
    property_type,
    bhk,
    size_sqft,
    property_age,
    furnishing,
    parking,
    metro_distance,
    school_distance,
    hospital_distance,
    location_rating,
    amenities_score
):
    if indian_model is None:
        raise RuntimeError(
            "Indian house model is unavailable. "
            "Run python train_indian_model.py first."
        )

    numerical = {
        "BHK": bhk,
        "Size_sqft": size_sqft,
        "Property_Age": property_age,
        "Parking": parking,
        "Metro_Distance_km": metro_distance,
        "School_Distance_km": school_distance,
        "Hospital_Distance_km": hospital_distance,
        "Location_Rating": location_rating,
        "Amenities_Score": amenities_score
    }

    categorical = {
        "City": city,
        "Locality": locality,
        "Property_Type": property_type,
        "Furnishing_Status": furnishing
    }

    input_data = pd.DataFrame([{
        **numerical,
        **categorical
    }])

    encoded = pd.get_dummies(
        input_data,
        columns=indian_model["categorical_features"],
        drop_first=True,
        dtype=float
    )

    encoded = encoded.reindex(
        columns=indian_model["features"],
        fill_value=0
    )

    values = encoded.to_numpy(dtype=float)

    means = np.array(indian_model["means"])
    stds = np.array(indian_model["stds"])
    coefficients = np.array(indian_model["coefficients"])

    scaled = (values - means) / stds

    prediction = (
        indian_model["intercept"]
        + np.dot(scaled[0], coefficients)
    )

    return float(prediction)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🏡 EstateIQ")
    st.caption("AI PROPERTY INTELLIGENCE")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📊 Price Analytics",
            "🕘 Prediction History",
            "📈 Dataset Analysis",
            "🤖 Model Information",
            "ℹ️ About Project"
        ]
    )
    

    st.divider()

    st.markdown("### Model Status")
    st.success("Prediction model loaded")

    st.caption("Algorithm: Linear Regression")
    st.caption("Engine: NumPy")

    st.divider()

    st.caption("Developed as an AI/ML portfolio project.")


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🏡 EstateIQ</h1>
    <p>AI-powered House Price Prediction & Property Intelligence Platform</p>
    <p>Make smarter property estimates using machine learning.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- DASHBOARD ----------------


if page == "🏠 Dashboard":

    st.title("🏡 EstateIQ - Indian House Price Prediction")
    st.write("AI-powered property price estimation using Indian housing data.")

    st.markdown("---")
    st.subheader("Enter Property Details")

    with st.form("indian_prediction_form"):

        col1, col2 = st.columns(2)

        with col1:
            city = st.selectbox("City", cities)

            localities = sorted(
                property_data[
                    property_data["City"] == city
                ]["Locality"].dropna().unique()
            )

            locality = st.selectbox("Locality", localities)

            property_type = st.selectbox(
                "Property Type", property_types
            )

            bhk = st.number_input(
                "BHK", min_value=1, max_value=5, value=2, step=1
            )

            size_sqft = st.number_input(
                "Property Size (sq. ft.)",
                min_value=450, max_value=3500, value=1000, step=50
            )

            property_age = st.number_input(
                "Property Age (years)",
                min_value=0, max_value=28, value=5, step=1
            )

            furnishing = st.selectbox(
                "Furnishing Status", furnishing_options
            )

        with col2:
            parking = st.number_input(
                "Parking Spaces",
                min_value=0, max_value=3, value=1, step=1
            )

            metro_distance = st.number_input(
                "Metro Distance (km)",
                min_value=0.2, max_value=12.0,
                value=2.0, step=0.1
            )

            school_distance = st.number_input(
                "School Distance (km)",
                min_value=0.2, max_value=6.0,
                value=1.0, step=0.1
            )

            hospital_distance = st.number_input(
                "Hospital Distance (km)",
                min_value=0.2, max_value=6.0,
                value=1.0, step=0.1
            )

            location_rating = st.number_input(
                "Location Rating",
                min_value=3, max_value=10, value=7, step=1
            )

            amenities_score = st.number_input(
                "Amenities Score",
                min_value=1, max_value=6, value=3, step=1
            )

        submitted = st.form_submit_button(
            "Predict Property Price",
            use_container_width=True
        )

    if submitted:

        predicted_price = predict_indian_price(
            city,
            locality,
            property_type,
            bhk,
            size_sqft,
            property_age,
            furnishing,
            parking,
            metro_distance,
            school_distance,
            hospital_distance,
            location_rating,
            amenities_score
        )

        record = {
            "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "locality": locality,
            "property_type": property_type,
            "bhk": bhk,
            "size_sqft": size_sqft,
            "property_age": property_age,
            "furnishing": furnishing,
            "parking": parking,
            "metro_distance": metro_distance,
            "school_distance": school_distance,
            "hospital_distance": hospital_distance,
            "location_rating": location_rating,
            "amenities_score": amenities_score,
            "predicted_price": predicted_price
        }

        save_indian_prediction(record)

        st.session_state["last_indian_prediction"] = record

        st.success("Prediction generated and saved successfully!")

    if "last_indian_prediction" in st.session_state:

        result = st.session_state["last_indian_prediction"]

        st.markdown("---")
        st.subheader("🏠 Estimated Property Price")

        st.metric(
            "Predicted Property Value",
            f"₹{result['predicted_price']:,.0f}"
        )

        st.write(f"**City:** {result['city']}")
        st.write(f"**Locality:** {result['locality']}")
        st.write(f"**Property Type:** {result['property_type']}")
        st.write(f"**BHK:** {result['bhk']}")
        st.write(f"**Area:** {result['size_sqft']} sq. ft.")

        st.caption(
            "This is an educational estimate based on the supplied dataset, "
            "not a verified market valuation."
        )


# ---------------- PRICE ANALYTICS ----------------


elif page == "📊 Price Analytics":

    st.subheader("📊 Indian Property Price Analytics")

    result = st.session_state.get("last_indian_prediction")

    st.markdown("### Dataset Price Overview")

    # Average price by city
    city_prices = (
        property_data.groupby("City")["Price"]
        .mean()
        .sort_values(ascending=False)
    )

    st.markdown("#### Average Property Price by City")
    st.bar_chart(city_prices)

    # Average price by BHK
    bhk_prices = (
        property_data.groupby("BHK")["Price"]
        .mean()
        .sort_index()
    )

    st.markdown("#### Average Property Price by BHK")
    st.line_chart(bhk_prices)

    # Property size versus price
    st.markdown("#### Property Size vs Property Price")

    size_data = property_data[
        ["Size_sqft", "Price"]
    ].sort_values("Size_sqft")

    st.scatter_chart(
        size_data,
        x="Size_sqft",
        y="Price"
    )

    st.divider()

    if result:

        st.markdown("### Current Prediction Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Estimated Price",
            f"₹{result['predicted_price']:,.0f}"
        )

        c2.metric(
            "Property Size",
            f"{result['size_sqft']:,} sq. ft."
        )

        price_per_sqft = (
            result["predicted_price"] / result["size_sqft"]
        )

        c3.metric(
            "Estimated Price per Sq. Ft.",
            f"₹{price_per_sqft:,.0f}"
        )

        st.write(f"**City:** {result['city']}")
        st.write(f"**Locality:** {result['locality']}")
        st.write(f"**BHK:** {result['bhk']}")

    else:

        st.info(
            "Generate a prediction on the Dashboard to view "
            "your current property metrics."
        )

    st.caption(
        "Charts use the supplied educational housing dataset. "
        "They describe the dataset and are not verified market prices."
    )

# ---------------- MODEL INFORMATION ----------------

# ---------------- PREDICTION HISTORY ----------------


elif page == "🕘 Prediction History":

    st.subheader("🕘 Indian Property Prediction History")
    st.write("Review all your saved Indian property price predictions.")

    history = get_indian_prediction_history()

    if not history.empty:

        history_df = history.copy()

        history_df = history_df.rename(columns={
            "id": "ID",
            "date": "Date",
            "city": "City",
            "locality": "Locality",
            "property_type": "Property Type",
            "bhk": "BHK",
            "size_sqft": "Size (sq. ft.)",
            "property_age": "Property Age",
            "furnishing": "Furnishing",
            "parking": "Parking",
            "metro_distance": "Metro Distance (km)",
            "school_distance": "School Distance (km)",
            "hospital_distance": "Hospital Distance (km)",
            "location_rating": "Location Rating",
            "amenities_score": "Amenities Score",
            "predicted_price": "Predicted Price"
        })

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Predictions", len(history_df))

        with col2:
            average_price = history_df["Predicted Price"].mean()
            st.metric(
                "Average Estimated Price",
                f"₹{average_price:,.0f}"
            )

        with col3:
            highest_price = history_df["Predicted Price"].max()
            st.metric(
                "Highest Estimated Price",
                f"₹{highest_price:,.0f}"
            )

        st.divider()

        st.markdown("### Previous Indian Property Predictions")

        st.dataframe(
            history_df,
            hide_index=True,
            use_container_width=True
        )

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Prediction History",
            data=csv,
            file_name="indian_prediction_history.csv",
            mime="text/csv"
        )

        if st.button("Clear Indian Prediction History"):
            clear_indian_prediction_history()
            st.success("Indian prediction history cleared!")
            st.rerun()

    else:
        st.info("No Indian property predictions available yet.")

    # Preserve access to old prediction records
    with st.expander("View Previous Legacy Predictions"):

        old_history = get_prediction_history()

        if not old_history.empty:

            st.dataframe(
                old_history,
                hide_index=True,
                use_container_width=True
            )

        else:
            st.info("No older predictions available.")


        # Download history
        st.download_button(
            label="⬇️ Download History as CSV",
            data=history_df.to_csv(index=False),
            file_name="estateiq_prediction_history.csv",
            mime="text/csv"
        )

        # Clear history
        if st.button("🗑️ Clear Prediction History"):
            clear_prediction_history()
            st.session_state["prediction_history"] = []
            st.success("Prediction history cleared!")
            st.rerun()

        else:

         st.info(
            "No prediction history available yet. "
            "Visit the Dashboard and generate your first prediction."
        )

# ---------------- DATASET ANALYSIS ----------------

elif page == "📈 Dataset Analysis":

    st.subheader("📈 Dataset Analysis")

    # Load dataset
    dataset = pd.read_csv(DATASET_PATH)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Properties", len(dataset))

    col2.metric(
        "Average Price",
        f"₹{dataset['Price'].mean():,.0f}"
    )

    col3.metric(
        "Minimum Price",
        f"₹{dataset['Price'].min():,.0f}"
    )

    col4.metric(
        "Maximum Price",
        f"₹{dataset['Price'].max():,.0f}"
    )

    st.divider()

    st.markdown("### Property Price Distribution")

    # Convert prices into lakhs for easier visualization
    chart_data = dataset.copy()
    chart_data["Price (Lakhs)"] = chart_data["Price"] / 100000

    st.bar_chart(
        chart_data,
        x="Area",
        y="Price (Lakhs)",
        alt="House prices by area in lakhs"
    )

    st.markdown("### Area vs House Price")

    st.scatter_chart(
        chart_data,
        x="Area",
        y="Price (Lakhs)",
        alt="Scatter chart of area versus house price"
    )

    st.markdown("### Dataset Overview")

    st.dataframe(
        dataset.describe(),
        alt="Summary statistics for the house dataset"
    )

    st.markdown("### Original Dataset Records")

    st.dataframe(
        dataset,
        hide_index=True,
        alt="Original house dataset records"
    )

    st.download_button(
        "⬇️ Download Dataset",
        data=dataset.to_csv(index=False),
        file_name="estateiq_dataset.csv",
        mime="text/csv"
    )

    st.warning(
        "This dataset contains 20 synthetic educational records. "
        "Its statistics should not be interpreted as actual property market data."
    )


elif page == "🤖 Model Information":

    st.subheader("🤖 Indian House Price Prediction Model")

    st.markdown("""
    <div class="section-card">
        <h3>Multiple Linear Regression</h3>
        <p>
        This model estimates property prices using multiple numerical
        and categorical property features. It is implemented using
        NumPy least-squares regression.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Model Configuration")

    st.write("**Algorithm:** Multiple Linear Regression")
    st.write("**Implementation:** NumPy least-squares method")
    st.write("**Dataset:** Indian House Prices (5,000 records)")
    st.write("**Training records:** 4,000")
    st.write("**Testing records:** 1,000")
    st.write("**Encoded input features:** 37")
    st.write("**Target variable:** Property Price")
    st.write("**Model storage:** JSON")

    st.divider()

    st.markdown("### Model Performance")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Test MAE", "₹14,86,614.90")

    with metric2:
        st.metric("Test RMSE", "₹20,15,747.77")

    with metric3:
        st.metric("Test R² Score", "0.9506")

    st.caption(
        "These are the reported held-out test results from the latest "
        "training run. The dataset is synthetic/educational, so these "
        "metrics do not establish real-world market accuracy."
    )

    st.divider()

    st.markdown("### Model Input Features")

    feature_data = pd.DataFrame({
        "Feature": indian_model["features"],
        "Coefficient": indian_model["coefficients"]
    })

    st.dataframe(
        feature_data,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "The coefficients represent the fitted model's standardized "
        "feature relationships. They do not establish causation."
    )


# ---------------- ABOUT PROJECT ----------------

elif page == "ℹ️ About Project":

    st.subheader("About EstateIQ")

    st.markdown("""
    <div class="section-card">
        <h3>Project Overview</h3>
        <p>
        EstateIQ is an educational machine-learning application that predicts
        estimated house prices based on property characteristics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Technology Stack")

    technologies = pd.DataFrame({
        "Technology": [
            "Python",
            "NumPy",
            "Pandas",
            "Streamlit",
            "Linear Regression",
            "JSON"
        ],
        "Purpose": [
            "Programming language",
            "Numerical computation and model training",
            "Dataset handling",
            "Interactive web application",
            "Prediction algorithm",
            "Model storage"
        ]
    })

    st.dataframe(
        technologies,
        hide_index=True,
        width="stretch"
    )

    st.markdown("### Project Workflow")

    st.write("""
    1. Collect and load sample property data.
    2. Prepare input features and target values.
    3. Train the Linear Regression model.
    4. Save the learned coefficients.
    5. Generate predictions for new property inputs.
    6. Display analytics and downloadable reports.
    """)

    st.warning(
        "The current dataset contains only 20 synthetic records. "
        "This project is a learning prototype, not a production property valuation system."
    )


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    ESTATEIQ • AI PROPERTY INTELLIGENCE<br>
    Built with Python, NumPy and Streamlit
</div>
""", unsafe_allow_html=True)
