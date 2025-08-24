import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import plotly.graph_objects as go

def render_retention_models(df_retention):
    st.header("📈 Talent Retention Predictive Models")
    
    # Préparation des données pour ML
    features = ['Salary_Percentile', 'Work_Life_Balance', 'Career_Growth', 'Manager_Quality', 'Is_Neurodivergent']
    X = df_retention[features]
    y = df_retention['Stayed']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entraînement du modèle
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Métriques du modèle
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Model Accuracy", f"{accuracy:.1%}", "ML Prediction")
    
    with col2:
        retention_rate = df_retention['Stayed'].mean()
        st.metric("Overall Retention", f"{retention_rate:.1%}", "Current Rate")
    
    with col3:
        neuro_retention = df_retention[df_retention['Is_Neurodivergent'] == 1]['Stayed'].mean()
        regular_retention = df_retention[df_retention['Is_Neurodivergent'] == 0]['Stayed'].mean()
        st.metric("Neurodivergent Advantage", f"+{(neuro_retention - regular_retention) * 100:.1f}%", "Retention Boost")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=True)
    
    fig_importance = px.bar(
        feature_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        title="🔍 Key Retention Factors - Feature Importance",
        labels={'Importance': 'Importance Score', 'Feature': 'Factors'}
    )
    fig_importance.update_layout(height=400)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # Analyse par département
    dept_retention = df_retention.groupby('Department').agg({
        'Stayed': 'mean',
        'Is_Neurodivergent': 'mean',
        'Salary_Percentile': 'mean'
    }).reset_index()
    
    fig_dept = px.scatter(
        dept_retention,
        x='Is_Neurodivergent',
        y='Stayed',
        size='Salary_Percentile',
        color='Department',
        title="📊 Department-Level Retention vs Neurodiversity",
        labels={'Is_Neurodivergent': 'Neurodiversity Rate', 'Stayed': 'Retention Rate'}
    )
    fig_dept.update_layout(height=400)
    st.plotly_chart(fig_dept, use_container_width=True)
    
    # Calculateur de risque interactif
    st.subheader("🎯 Employee Retention Risk Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        salary_input = st.slider("Salary Percentile", 20, 95, 60)
        wlb_input = st.slider("Work-Life Balance (1-5)", 1.0, 5.0, 3.5, 0.1)
        career_input = st.slider("Career Growth Score (1-5)", 1.0, 5.0, 3.0, 0.1)
    
    with col2:
        manager_input = st.slider("Manager Quality (1-5)", 1.0, 5.0, 3.5, 0.1)
        neuro_input = st.selectbox("Neurodivergent", ["No", "Yes"])
        neuro_binary = 1 if neuro_input == "Yes" else 0
    
    # Prédiction en temps réel
    prediction_input = [[salary_input, wlb_input, career_input, manager_input, neuro_binary]]
    proba = model.predict_proba(prediction_input)
    if proba.shape[1] >= 2:
        retention_prob = proba[0][1]
    else:
        retention_prob = proba[0][0]
    
    st.metric("Retention Probability", f"{retention_prob:.1%}", "Predicted Likelihood")
    
    if retention_prob < 0.6:
        st.error("⚠️ High Risk - Immediate intervention recommended")
    elif retention_prob < 0.8:
        st.warning("⚡ Medium Risk - Monitor closely")
    else:
        st.success("✅ Low Risk - Employee likely to stay")

