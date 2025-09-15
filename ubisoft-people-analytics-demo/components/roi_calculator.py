import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_roi_calculator_improved(df_roi):
    st.header("💰 ROI Calculator - Retention & Diversity Programs")
    
    # ========== SECTION 1: INTÉGRATION AVEC LE MODÈLE DE RÉTENTION ==========
    
    st.subheader("🎯 ML-Powered ROI Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**🤖 Modèle ML Integration**")
        st.write("Utilise les prédictions du modèle de rétention sans fuite pour calculer un ROI précis")
        
        # Simulation des prédictions du modèle (à connecter avec retention_models.py)
        high_risk_employees = st.number_input("Employés à haut risque (ML)", 20, 200, 75, 
                                            help="Identifiés par le modèle de rétention")
        
        medium_risk_employees = st.number_input("Employés à risque modéré (ML)", 50, 300, 120)
        
        model_accuracy = st.slider("Précision du modèle ML", 0.6, 0.95, 0.82, 0.01,
                                 help="AUC score du modèle de rétention")
    
    with col2:
        st.info("**💼 Paramètres Entreprise**")
        company_size = st.number_input("Taille entreprise", 500, 5000, 1200)
        avg_salary = st.number_input("Salaire moyen (€)", 40000, 120000, 75000)
        current_turnover = st.slider("Taux turnover actuel (%)", 5, 30, 15)
    
    # ========== SECTION 2: PARAMÈTRES PROGRAMME ==========
    
    st.subheader("🎛️ Program Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**💰 Investissements**")
        program_investment = st.number_input("Investment programme (€)", 10000, 500000, 150000)
        cost_per_intervention = st.number_input("Coût par intervention (€)", 2000, 15000, 6000)
        implementation_months = st.slider("Durée implémentation (mois)", 3, 24, 12)
    
    with col2:
        st.write("**🎯 Efficacité Ciblage**")
        intervention_success_rate = st.slider("Taux succès intervention", 0.2, 0.8, 0.45, 0.05)
        targeting_precision = st.slider("Précision ciblage", 0.6, 0.95, 0.78, 0.01,
                                       help="% d'employés réellement à risque parmi ceux ciblés")
    
    with col3:
        st.write("**📊 Impact Différentiel**")
        neuro_retention_boost = st.slider("Boost rétention neurodivergents (%)", 5, 40, 18, 1)
        regular_retention_boost = st.slider("Boost rétention autres (%)", 3, 25, 12, 1)
    
    # ========== SECTION 3: CALCULS ROI AVANCÉS ==========
    
    # Coût de remplacement par employé
    replacement_cost_multiplier = 1.8  # Recherche indique 1.5-2x salaire
    cost_per_departure = avg_salary * replacement_cost_multiplier
    
    # Calcul des employés qui seraient partis sans intervention
    baseline_departures_high = high_risk_employees * 0.75 * targeting_precision
    baseline_departures_medium = medium_risk_employees * 0.45 * targeting_precision
    total_baseline_departures = baseline_departures_high + baseline_departures_medium
    
    # Employés sauvés grâce à l'intervention
    employees_saved = total_baseline_departures * intervention_success_rate
    
    # Économies totales
    total_savings = employees_saved * cost_per_departure
    
    # Coûts du programme
    employees_targeted = high_risk_employees + medium_risk_employees
    total_intervention_cost = employees_targeted * cost_per_intervention
    total_program_cost = program_investment + total_intervention_cost
    
    # ROI net et métriques
    net_roi = total_savings - total_program_cost
    roi_percentage = (net_roi / total_program_cost) * 100 if total_program_cost > 0 else 0
    
    # ========== SECTION 4: AFFICHAGE RÉSULTATS ==========
    
    st.subheader("📊 ROI Analysis Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Économies Totales",
            f"€{total_savings:,.0f}",
            f"{employees_saved:.0f} employés sauvés"
        )
    
    with col2:
        st.metric(
            "📈 ROI Net (An 1)",
            f"€{net_roi:,.0f}",
            f"{roi_percentage:.0f}% retour"
        )
    
    with col3:
        payback_months = (total_program_cost / (total_savings / 12)) if total_savings > 0 else float('inf')
        st.metric(
            "⏱️ Récupération",
            f"{payback_months:.1f} mois" if payback_months != float('inf') else "N/A",
            "Break-even"
        )
    
    with col4:
        confidence_score = model_accuracy * targeting_precision * intervention_success_rate
        st.metric(
            "🎯 Score Confiance",
            f"{confidence_score:.1%}",
            "Fiabilité prédiction"
        )
    
    # ========== SECTION 5: GRAPHIQUES AVANCÉS ==========
    
    # Graphique de sensibilité multi-variables
    st.subheader("📊 Analyse de Sensibilité Multi-Variables")
    
    sensitivity_var = st.selectbox(
        "Variable à analyser",
        ["Taux succès intervention", "Précision ciblage", "Coût intervention", "Précision modèle ML"]
    )
    
    if sensitivity_var == "Taux succès intervention":
        x_values = np.arange(0.2, 0.8, 0.02)
        roi_values = []
        for rate in x_values:
            saved = total_baseline_departures * rate
            savings = saved * cost_per_departure
            roi = ((savings - total_program_cost) / total_program_cost) * 100
            roi_values.append(roi)
        x_label = "Taux de Succès"
    
    elif sensitivity_var == "Précision ciblage":
        x_values = np.arange(0.5, 0.95, 0.01)
        roi_values = []
        for precision in x_values:
            baseline_deps = (high_risk_employees * 0.75 + medium_risk_employees * 0.45) * precision
            saved = baseline_deps * intervention_success_rate
            savings = saved * cost_per_departure
            roi = ((savings - total_program_cost) / total_program_cost) * 100
            roi_values.append(roi)
        x_label = "Précision Ciblage"
    
    fig_sensitivity = go.Figure()
    fig_sensitivity.add_trace(go.Scatter(
        x=x_values * 100,
        y=roi_values,
        mode='lines+markers',
        name='ROI %',
        line=dict(color='#667eea', width=3),
        marker=dict(size=6)
    ))
    
    fig_sensitivity.add_hline(y=0, line_dash="dash", line_color="red", 
                            annotation_text="Seuil de rentabilité")
    fig_sensitivity.add_hline(y=100, line_dash="dot", line_color="green", 
                            annotation_text="ROI 100%")
    
    fig_sensitivity.update_layout(
        title=f"Impact de '{sensitivity_var}' sur le ROI",
        xaxis_title=f"{x_label} (%)",
        yaxis_title="ROI (%)",
        height=400
    )
    
    st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    # ========== SECTION 6: RECOMMANDATIONS STRATÉGIQUES ==========
    
    st.subheader("🎯 Recommandations Stratégiques ML-Driven")
    
    if roi_percentage > 200:
        st.success("🚀 **ROI Exceptionnel** - Programme hautement rentable ! Déployez rapidement.")
        priority = "HAUTE"
    elif roi_percentage > 100:
        st.info("💡 **ROI Solide** - Investissement judicieux avec retours mesurables.")
        priority = "MOYENNE"
    elif roi_percentage > 0:
        st.warning("⚠️ **ROI Modéré** - Optimisez les paramètres avant déploiement.")
        priority = "FAIBLE"
    else:
        st.error("❌ **ROI Négatif** - Revisitez la stratégie d'intervention.")
        priority = "CRITIQUE"
    
    recommendations = [
        f"🎯 **Ciblage ML**: Le modèle identifie {high_risk_employees} employés prioritaires (précision {model_accuracy:.1%})",
        f"💰 **Budget Optimal**: {total_program_cost:,.0f}€ pour sauver ~{employees_saved:.0f} employés",
        f"📊 **Monitoring**: Tracker mensuellement la rétention pour valider l'efficacité",
        f"🔄 **Itération**: Réentraîner le modèle tous les 6 mois avec nouvelles données",
        f"🎮 **Scaling Ubisoft**: Succès ici = expansion possible aux autres studios globalement"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.info(f"**{i}.** {rec}")
    
    # Score final et next steps
    st.subheader("📋 Next Steps")
    
    if priority == "HAUTE":
        next_steps = [
            "✅ Valider le budget avec la direction",
            "🚀 Lancer le programme pilote sur 3 mois",
            "📊 Mettre en place le monitoring temps réel",
            "🎯 Former les équipes RH sur l'utilisation du modèle ML"
        ]
    elif priority == "MOYENNE":
        next_steps = [
            "🔧 Optimiser les paramètres d'intervention",
            "📊 Tester sur un échantillon réduit",
            "💡 Améliorer la précision du modèle ML",
            "📈 Ré-évaluer le ROI après ajustements"
        ]
    else:
        next_steps = [
            "🔍 Analyser les causes du ROI faible",
            "💰 Réviser les coûts d'intervention",
            "🎯 Améliorer l'efficacité du ciblage ML",
            "📊 Benchmarker avec d'autres approches"
        ]
    
    for step in next_steps:
        st.write(f"• {step}")

# Fonction de compatibilité avec l'ancien nom
def render_roi_calculator(df_roi):
    return render_roi_calculator_improved(df_roi)
