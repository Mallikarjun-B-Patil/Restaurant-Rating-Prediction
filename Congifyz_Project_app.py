import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# -------------------
# Load and preprocess dataset
# -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    return df

df = load_data()

st.title("🍽️ Restaurant Rating Prediction")
st.write("Predict the **Aggregate Rating** of a restaurant based on its features.")

# -------------------
# Preprocessing function
# -------------------
def preprocess_data(df):
    df = df.copy()
    
    # Keep only necessary columns
    necessary_cols = ['City', 'Cuisines', 'Price range', 'Votes', 'Aggregate rating']
    df = df[necessary_cols]
    
    # Handle missing values using KNN Imputer for numeric columns
    imputer = KNNImputer(n_neighbors=3)
    numeric_cols = ['Price range', 'Votes']
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    
    # Encode categorical features
    label_encoders = {}
    for col in ['City', 'Cuisines']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    return df, label_encoders

processed_df, label_encoders = preprocess_data(df)

# Features and Target
X = processed_df.drop(columns=['Aggregate rating'])
y = processed_df['Aggregate rating']

# Scale numeric features
scaler = StandardScaler()
X[X.columns] = scaler.fit_transform(X[X.columns])

# Train model
model = LinearRegression()
model.fit(X, y)

# -------------------
# User Input Section
# -------------------
st.header("Enter Restaurant Details")

# User input fields
city = st.selectbox("City", list(label_encoders['City'].classes_))
cuisine = st.selectbox("Cuisine", list(label_encoders['Cuisines'].classes_))
price_range = st.number_input("Price Range (1 to 4)", min_value=1, max_value=4, value=2)
votes = st.number_input("Number of Votes", min_value=0, max_value=int(df['Votes'].max()), value=10)

# Convert user input into DataFrame
input_data = pd.DataFrame({
    'City': [city],
    'Cuisines': [cuisine],
    'Price range': [price_range],
    'Votes': [votes]
})

# Encode categorical features
input_data['City'] = label_encoders['City'].transform(input_data['City'])
input_data['Cuisines'] = label_encoders['Cuisines'].transform(input_data['Cuisines'])

# Scale numeric features
input_data[X.columns] = scaler.transform(input_data[X.columns])

# Prediction
if st.button("Predict Rating"):
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Aggregate Rating: **{round(prediction, 2)}** ⭐")
