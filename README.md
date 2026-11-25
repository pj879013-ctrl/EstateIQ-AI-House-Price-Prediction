# 🏡 EstateIQ – AI House Price Intelligence

### AI-Powered Indian House Price Prediction System

EstateIQ is a machine learning-based web application that predicts residential property prices using property characteristics and location-related features.

The application uses a Multiple Linear Regression model implemented with NumPy and provides an interactive dashboard built with Streamlit.

---

## 🚀 Project Overview

EstateIQ helps users estimate residential property prices by entering details such as:

- City and locality
- Property type
- Number of bedrooms (BHK)
- Property size
- Property age
- Furnishing status
- Parking availability
- Distance from metro, schools and hospitals
- Location rating
- Amenities score

The system generates an estimated property price and stores prediction history using SQLite.

## ✨ Key Features

### 1. Interactive Prediction Dashboard
- Enter 13 property details.
- Select cities, localities and property types.
- Generate estimated property prices.
- View the estimated price per square foot.

### 2. Price Analytics
- Average property prices by city.
- Price comparisons by BHK.
- Property size versus price visualization.
- Interactive charts.

### 3. Prediction History
- Store predictions permanently using SQLite.
- View previous predictions.
- Calculate average and highest estimated prices.
- Download prediction history as CSV.

### 4. Dataset Analysis
- Explore the housing dataset.
- Analyze property characteristics.
- View numerical and categorical distributions.

### 5. Model Information
- View model configuration.
- Examine model performance metrics.
- Explore learned feature coefficients.

---

## 🧠 Machine Learning Model

**Algorithm:** Multiple Linear Regression  
**Implementation:** NumPy least-squares method  
**Dataset size:** 5,000 records  
**Training data:** 4,000 records  
**Testing data:** 1,000 records  
**Encoded features:** 37  
**Target variable:** Property Price

### Model Evaluation

| Evaluation Metric | Result |
|---|---:|
| MAE | ₹14,86,614.90 |
| RMSE | ₹20,15,747.77 |
| R² Score | 0.9506 |

*These results are from the reported held-out test run. The supplied dataset is synthetic/educational, so the metrics do not establish real-world property valuation accuracy.*

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| NumPy | Numerical computation and model training |
| Pandas | Dataset processing |
| Streamlit | Web application |
| SQLite | Prediction history database |
| Matplotlib / Streamlit charts | Data visualization |
| JSON | Model storage |

---

## 📂 Project Structure

```text
House_Price_prediction/
│
├── app.py
├── main.py
├── train_model.py
├── train_indian_model.py
│
├── dataset/
│   ├── house_data.csv
│   └── indian_house_prices.csv
│
├── models/
│   ├── house_price_model.json
│   └── indian_house_model.json
│
├── README.md
├── requirements.txt
└── .venv/
```

*The structure above is a guide; adjust it to match the actual files in your repository.*

---

## ⚙️ Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd House_Price_prediction
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 📊 Application Modules

1. Dashboard
2. Price Analytics
3. Prediction History
4. Dataset Analysis
5. Model Information
6. About Project

---

## 🎯 Project Objective

The objective of EstateIQ is to demonstrate how machine learning, numerical computing, data analysis and interactive web development can be combined to build a property price estimation application.

## 🔮 Future Enhancements

- Integrate real-world verified property datasets.
- Experiment with additional regression algorithms.
- Improve model evaluation and validation.
- Add interactive location-based property analysis.
- Deploy the application online.
- Add user authentication and personalized dashboards.

## ⚠️ Disclaimer

EstateIQ is an educational machine learning project. Its price predictions are estimates based on the supplied dataset and should not be treated as verified property valuations or financial advice.

## 👩‍💻 Project Information

**Project Name:** EstateIQ – AI House Price Intelligence  
**Domain:** Artificial Intelligence and Machine Learning  
**Application Type:** Web-Based Machine Learning Application  
**Developer:** Pratiksha Jadhav


---

⭐ If you find this project interesting, consider giving the repository a star!
