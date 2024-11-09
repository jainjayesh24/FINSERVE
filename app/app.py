import streamlit as st
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model

model = load_model('app/Upmodel.h5')

with open('app/label2.pkl', 'rb') as f:
    label2 = pickle.load(f)

with open('app/label.pkl', 'rb') as f:
    label = pickle.load(f)

with open('app/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

st.set_page_config(page_title="Churn Predictor", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 5px;
        padding: 12px 24px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox, .stSlider, .stNumberInput {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stSelectbox>label, .stSlider>label, .stNumberInput>label {
        color: #333;
        font-size: 16px;
    }
    h1 {
        color: #4CAF50;
    }
    .prediction-output {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .prediction-output h3 {
        font-size: 20px;
    }
    .prediction-output p {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.title('Churn Predictor: Analyze & Forecast Customer Retention')
st.markdown("Use this tool to predict the likelihood of customer churn and take necessary actions.")

col1, col2 = st.columns(2)

with col1:
    geography = st.selectbox('Geography', label2.categories_[0])
    gender = st.selectbox('Gender', label.classes_)
    age = st.slider('Age', 18, 92)
    balance = st.number_input('Balance', min_value=0, value=1000)
    credit_score = st.number_input('Credit Score', min_value=300, value=650)

with col2:
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=50000.0)
    tenure = st.slider('Tenure', 0, 10)
    num_of_products = st.slider('Number of Products', 1, 4)
    has_cr_card = st.selectbox('Has Credit Card', [0, 1])
    is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label.transform([gender])[0]],  # Encode gender
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

geo_encoded = label2.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=label2.get_feature_names_out(['Geography']))
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

input_data_scaled = scaler.transform(input_data)

input_data_scaled = input_data_scaled.reshape(1, -1)

prediction = model.predict(input_data_scaled)
prediction_proba = prediction[0][0]

with st.container():
    st.markdown('<div class="prediction-output">', unsafe_allow_html=True)
    st.write(f'### Churn Probability: {prediction_proba:.2f}')
    if prediction_proba > 0.5:
        st.write('**Red Flag: Potential Customer Loss Detected!**')
        st.markdown('<p style="color: red;">Take immediate actions to retain the customer.</p>', unsafe_allow_html=True)
    else:
        st.write('**All Clear: Customer Retention Likely!**')
        st.markdown('<p style="color: green;">The customer is likely to stay.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
