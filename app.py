import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown(
    """
    <style>
    /* Change the entire background */
    body {
        background-color: #00605F !important;
        color: #ffffff !important;
    }

    /* Change sidebar background */
    [data-testid="stSidebar"] {
        background-color: #008081 !important;
    }

    /* Change headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00C1C0 !important;
    }

    /* Style buttons */
    .stButton>button {
        background-color: #00A0A0 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid #00C1C0 !important;
        font-size: 16px !important;
    }

    /* Style text input fields */
    .stTextInput>div>div>input {
        background-color: #004F4E !important;
        color: #ffffff !important;
        border: 2px solid #00C1C0 !important;
        border-radius: 5px !important;
    }

    /* Style select boxes */
    .stSelectbox>div>div {
        background-color: #004F4E !important;
        color: #ffffff !important;
        border-radius: 5px !important;
        border: 2px solid #00C1C0 !important;
    }

    /* Style tables */
    .stDataFrame {
        background-color: #004F4E !important;
        color: white !important;
    }
    
    /* Modify checkbox styles */
    .stCheckbox>div {
        color: #00C1C0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

import numpy as np

def karasek_chart(data):
    """
    Generate and display a Karasek quadrant graph in Streamlit.
    
    Parameters:
    - data (DataFrame): Data containing stress, anxiety, job control, and other related fields.
    """
    # Mapping categorical values to numeric for computation
    anxiete_mapping = {"Jamais": 1, "Parfois": 2, "Souvent": 3, "Très souvent": 4}
    clarte_mapping = {"Pas du tout clairs": 1, "Peu clairs": 2, "Assez clairs": 3, "Très clairs": 4}
    competences_mapping = {"Non": 1, "Partiellement": 2, "Oui": 3}

    # Ensure mappings exist
    if data.empty:
        st.warning("Aucune donnée disponible pour générer le graphique Karasek.")
        return

    # Convert categorical columns to numerical values
    data["Anxiété charge travail"] = data["Anxiété charge travail"].map(anxiete_mapping)
    data["Clarté objectifs"] = data["Clarté objectifs"].map(clarte_mapping)
    data["Compétences nécessaires"] = data["Compétences nécessaires"].map(competences_mapping)

    # Handle missing values
    data.fillna(0, inplace=True)

    # Calculate Job Demand & Job Control
    data["Job Demand"] = (data["Niveau de stress"] + data["Anxiété charge travail"]) / 2
    data["Job Control"] = (data["Clarté objectifs"] + data["Soutien équipe"] + data["Compétences nécessaires"]) / 3
    data["sem"] = data["Semaine"]
    # Define quadrant boundaries (Median Split)
    median_demand = np.median(data["Job Demand"])
    median_control = np.median(data["Job Control"])
    
    # Categorize individuals based on Karasek model
    def classify_karasek(row):
        if row["Job Demand"] >= median_demand and row["Job Control"] < median_control:
            return "Stressé"
        elif row["Job Demand"] >= median_demand and row["Job Control"] >= median_control:
            return "Actif"
        elif row["Job Demand"] < median_demand and row["Job Control"] < median_control:
            return "Passif"
        else:
            return "Détendu"

    data["Karasek Category"] = data.apply(classify_karasek, axis=1)

    # Create scatter plot
    fig_karasek = px.scatter(
        data,
        x="Job Control",
        y="Job Demand",
        color="Karasek Category",
        hover_data=["Nom", "Semaine"],
        title="Classification selon le modèle de Karasek",
        labels={"Job Control": "Contrôle du travail", "Job Demand": "Exigence du travail",},
        color_discrete_map={"Stressé": "red", "Actif": "green", "Passif": "blue", "Détendu": "orange"}
    )

    # Add quadrant lines
    fig_karasek.add_vline(x=median_control, line_dash="dash", line_color="white")
    fig_karasek.add_hline(y=median_demand, line_dash="dash", line_color="white")

    # Display the graph in Streamlit
    st.plotly_chart(fig_karasek, use_container_width=True)


# Nom du fichier CSV
DATA_FILE = "data.csv"

# Définition des colonnes attendues
COLUMNS = [
    'Nom', 'Niveau de stress', 'Accompagnement tuteur', 'Intérêt missions', 'Difficulté tâches',
    'Respect délais', 'Temps conciliation', 'Anxiété charge travail', 'Soutien équipe',
    'Compétences nécessaires', 'Clarté objectifs','Remarque', 'Semaine'
]


# Fonction pour charger les données depuis le CSV
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            data = pd.read_csv(DATA_FILE)
            # S'assurer que toutes les colonnes sont présentes
            for col in COLUMNS:
                if col not in data.columns:
                    data[col] = ""
            return data[COLUMNS]
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")
            return pd.DataFrame(columns=COLUMNS)
    else:
        return pd.DataFrame(columns=COLUMNS)

# Fonction pour sauvegarder les données dans le CSV
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Chargement initial dans la session
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Page d'accueil
def home_page():
    st.title("Bienvenue sur l'application de suivi des collaborateurs")
    st.write("""
    Cette application permet aux collaborateurs de saisir leurs données de satisfaction 
    et de bien-être au travail, et aux managers de visualiser et analyser ces données.
    """)
    st.write("Veuillez sélectionner votre rôle dans la barre latérale pour commencer.")

st.sidebar.image("/Users/abakarmahamatnezir/Documents/HETIC2024/S1/INTRO MANAGEMENT/ZenWork/image/image_3.png",use_container_width=True,)





# Barre latérale pour choisir le rôle
role = st.sidebar.radio("Choisissez votre rôle", ["Accueil", "Collaborateur", "Manager"])

if role == "Accueil":
    home_page()

elif role == "Collaborateur":
        # Option de l'utilisateur : Nouvel utilisateur ou utilisateur existant
    option = st.radio("Choisissez une option", ("Nouvel utilisateur", "Utilisateur existant"))

    if option == "Nouvel utilisateur":
        # Demande à l'utilisateur d'entrer son nom
        nom_utilisateur = st.text_input("Entrez votre nom :")

        

    if option == "Utilisateur existant":
        if st.session_state.data.empty:
            st.warning("Aucun utilisateur existant. Veuillez créer un nouvel utilisateur.")
        else:
            utilisateurs = st.session_state.data['Nom'].unique()
            selected_user = st.selectbox("Sélectionnez votre nom :", utilisateurs)
            nom = selected_user
            st.success(f"Bienvenue {selected_user}!")
            st.write("Voici vos informations enregistrées :")
            st.dataframe(st.session_state.data[st.session_state.data['Nom'] == selected_user])

    else:  # Création d'un nouvel utilisateur
        st.subheader("Création d'un nouvel utilisateur")
        nom = nom_utilisateur
    
    with st.form("creation_utilisateur_form", clear_on_submit=True):
        
        
        niveau_stress = st.slider("Niveau de stress (1-10)", 1, 10, 5)
        accompagnement_tuteur = st.selectbox("Accompagnement tuteur", ["Oui", "Non", "Partiellement"])
        interet_missions = st.slider("Intérêt missions (1-5)", 1, 5, 3)
        difficulte_taches = st.selectbox("Difficulté tâches", ["Trop faciles", "Adaptées", "Trop difficiles"])
        respect_delais = st.selectbox("Respect délais", ["Toujours", "Souvent", "Parfois", "Rarement"])
        temps_conciliation = st.selectbox("Temps conciliation", ["Oui", "Non", "Partiellement"])
        anxiete_charge_travail = st.selectbox("Anxiété charge travail", ["Jamais", "Parfois", "Souvent", "Très souvent"])
        soutien_equipe = st.slider("Soutien équipe (1-5)", 1, 5, 3)
        competences_necessaires = st.selectbox("Compétences nécessaires", ["Oui", "Non", "Partiellement"])
        clarte_objectifs = st.selectbox("Clarté objectifs", ["Très clairs", "Assez clairs", "Peu clairs", "Pas du tout clairs"])
        remarque = st.text_area("Remarque")
        
        if option == "Nouvel utilisateur":
            semaine = st.text_input("Numéro de semaine")
            if semaine.strip() == "":
                semaine = 1
        else:
            semaine = st.session_state.data[st.session_state.data['Nom'] == selected_user]['Semaine'].astype(int).max() + 1
        
        # Bouton de submit
        submit = st.form_submit_button("Créer l'utilisateur")
        
                
        
        
        if submit:
            if nom.strip() == "":
                st.error("Veuillez saisir un nom.")
            else:
                new_entry = {
                    'Nom': nom,
                    'Niveau de stress': niveau_stress,
                    'Accompagnement tuteur': accompagnement_tuteur,
                    'Intérêt missions': interet_missions,
                    'Difficulté tâches': difficulte_taches,
                    'Respect délais': respect_delais,
                    'Temps conciliation': temps_conciliation,
                    'Anxiété charge travail': anxiete_charge_travail,
                    'Soutien équipe': soutien_equipe,
                    'Compétences nécessaires': competences_necessaires,
                    'Clarté objectifs': clarte_objectifs,
                    'Remarque': remarque,
                    'Semaine': semaine
                }
                new_row = pd.DataFrame([new_entry])
                st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                save_data(st.session_state.data)
                st.success("Utilisateur créé avec succès!")

elif role == "Manager":
    st.title("Espace Manager")
    st.write("Voici l'ensemble des données collectées :")
    
    # Sélectionner si l'on veut afficher les données pour tout le monde ou pour un utilisateur spécifique
    user_option = st.selectbox(
        "Choisir un utilisateur ou afficher les données pour tous :",
        options=["Tous les utilisateurs"] + st.session_state.data["Nom"].unique().tolist()
    )

    # Filtrer les données en fonction de l'option choisie
    if user_option == "Tous les utilisateurs":
        data_display = st.session_state.data.reset_index(drop=True)
    else:
        data_display = st.session_state.data[st.session_state.data["Nom"] == user_option].reset_index(drop=True)

    st.dataframe(data_display)
    
    st.subheader("Visualisations")
    if not st.session_state.data.empty:
        # Histogramme du niveau de stress
        #fig1 = px.histogram(data_display, x="Niveau de stress", nbins=10, title="Distribution du Niveau de stress")
        #st.plotly_chart(fig1)
        high_risk = data_display[
            (data_display["Niveau de stress"] >= 8) & 
            (data_display["Anxiété charge travail"].isin(["Souvent", "Très souvent"])) & 
            (data_display["Soutien équipe"] <= 2) &
            (data_display["Intérêt missions"] <= 2)
        ]

        st.write("🚨 **Utilisateurs à risque de burnout:**")
        st.dataframe(high_risk)
        
        stress_counts = data_display["Niveau de stress"].value_counts().sort_index()

        fig1 = px.histogram(
            data_display, 
            x="Niveau de stress", 
            nbins=10, 
            
            title="Distribution du Niveau de stress",
            color_discrete_sequence=["royalblue"]  # Couleur des barres
        )

        # Ajouter des bordures aux colonnes
        fig1.update_traces(marker_line=dict(width=1.5, color="black"))


        
        # Diagramme circulaire pour l'accompagnement tuteur
        fig2 = px.pie(data_display, names="Accompagnement tuteur", title="Répartition de l'accompagnement par le tuteur")


        fig3 = px.sunburst(data_display, path=["Accompagnement tuteur", "Clarté objectifs", "Intérêt missions"], 
                           values="Soutien équipe",
                           title="Impact de l'accompagnement et des objectifs sur l'intérêt des missions")
    
        # Scatter Plot comparant le respect des délais et l'anxiété liée à la charge de travail
        fig4 = px.scatter(
            data_display,
            x="Respect délais",
            y="Anxiété charge travail",
            color="Nom",
            title="Corrélation entre le respect des délais et l'anxiété liée à la charge de travail",
            hover_data=["Nom"]
        )
        
        
        
        # Affichage du graphique avec Streamlit
        
        fig6 = px.line(data_display.groupby("Semaine")["Niveau de stress"].mean().reset_index(), 
              x="Semaine", y="Niveau de stress", 
              title="Évolution du niveau de stress par semaine", markers=True)


        fig7 = px.box(data_display, x="Accompagnement tuteur", y="Niveau de stress", 
             title="Impact de l'accompagnement sur le stress", color="Accompagnement tuteur")

        fig8 = px.box(data_display, x="Clarté objectifs", y="Niveau de stress", 
                     title="Impact de la clarté des objectifs sur le stress", color="Clarté objectifs")

        st.plotly_chart(fig6, use_container_width=True)


        # Create two columns
        col1, col2 = st.columns(2)

        # Add plots to columns in an alternating order
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.plotly_chart(fig7, use_container_width=True)

        with col2:
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig4, use_container_width=True)
            st.plotly_chart(fig8, use_container_width=True)
            
        user_option = st.selectbox(
        "Choisir un utilisateur ou afficher les données pour tous :",
        options=["Tous les utilisateurs"] + st.session_state.data["Nom"].unique().tolist(),
        key="user_selectbox_2"    )
        if user_option == "Tous les utilisateurs":
            data_display = st.session_state.data.reset_index(drop=True)
        else:
            data_display = st.session_state.data[st.session_state.data["Nom"] == user_option].reset_index(drop=True)
        #Scatter Plot montrant l'évolution du stress par semaine pour chaque personne
        fig_stress = px.line(
            data_display,
            x="Semaine",  # Colonne avec les semaines
            y="Niveau de stress",  # Colonne avec les niveaux de stress
            color="Nom",  # Colonne avec le nom de la personne
            title="Évolution du Niveau de Stress au Fil des Semaines",
            hover_data=["Nom", "Semaine", "Niveau de stress"],  # Informations affichées au survol
            labels={"Semaine": "Semaine", "Niveau de stress": "Niveau de Stress"}
        )
        st.plotly_chart(fig_stress)



        
        # Affichage du graphique Karasek
        karasek_chart(data_display)
    

        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        
        # Convert categorical variables to numerical
        data_display2 = st.session_state.data.reset_index(drop=True)
        df_ml = data_display2.copy()
        df_ml["Accompagnement tuteur"] = df_ml["Accompagnement tuteur"].map({"Oui": 1, "Non": 0, "Partiellement": 0.5})
        df_ml["Temps conciliation"] = df_ml["Temps conciliation"].map({"Oui": 1, "Non": 0})
        df_ml["Compétences nécessaires"] = df_ml["Compétences nécessaires"].map({"Oui": 1, "Non": 0})
        df_ml["Respect délais"] = df_ml["Respect délais"].map({"Toujours": 1, "Souvent": 0.75, "Parfois": 0.5, "Rarement": 0.25})
        df_ml["Clarté objectifs"] = df_ml["Clarté objectifs"].map({"Très clairs": 1, "Assez clairs": 0.75, "Peu clairs": 0.5, "Pas du tout clairs": 0.25})
        
        # Define X (features) and Y (target)
        X = df_ml[["Accompagnement tuteur", "Temps conciliation", "Compétences nécessaires", "Respect délais", "Clarté objectifs"]]
        y = (df_ml["Niveau de stress"] >= 8).astype(int)  # 1 if stress is high, 0 otherwise
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestClassifier(n_estimators=1000, random_state=420)
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Show accuracy
        st.write(f"📊 **Précision du modèle:** {accuracy_score(y_test, y_pred) * 100:.2f}%")
        
        # Identify users likely to have stress in the next week
        df_ml["Predicted Stress"] = model.predict(X)
        st.write("🚨 **Utilisateurs susceptibles d'avoir du stress élevé la semaine prochaine:**")
        st.dataframe(df_ml[df_ml["Predicted Stress"] == 1][["Nom", "Semaine"]])
        


    else:
        st.info("Aucune donnée n'a encore été enregistrée.")
    
    st.subheader("Modification des données")
    # Sélection des lignes à supprimer
    to_delete = st.multiselect(
        "Sélectionnez les indices des lignes à supprimer :",
        options=list(data_display.index)
    )
    if st.button("Supprimer les lignes sélectionnées"):
        if to_delete:
            data_display = data_display.drop(to_delete)
            data_display.reset_index(drop=True, inplace=True)
            st.session_state.data = data_display.copy()
            save_data(st.session_state.data)
            st.success("Lignes supprimées!")
            st.dataframe(data_display)
        else:
            st.warning("Aucune ligne sélectionnée.")
    
    if st.button("Réinitialiser le fichier (tout effacer)"):
        st.warning("Vous êtes sur le point de réinitialiser toutes les données. Cette action est irréversible.")
        if st.button("Confirmer la réinitialisation"):
            st.session_state.data = pd.DataFrame(columns=COLUMNS)
            save_data(st.session_state.data)
            st.success("Fichier réinitialisé!")
        else:
            st.info("Réinitialisation annulée.")



