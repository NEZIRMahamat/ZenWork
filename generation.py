import pandas as pd
import random
from faker import Faker

# Initialisation
fake = Faker()
Faker.seed(42)
random.seed(42)

# Définition des colonnes
columns = [
    'Nom', 'Niveau de stress', 'Accompagnement tuteur', 'Intérêt missions',
    'Difficulté tâches', 'Respect délais', 'Temps conciliation',
    'Anxiété charge travail', 'Soutien équipe', 'Compétences nécessaires',
    'Clarté objectifs', 'Remarque', 'Semaine'
]

# Génération des noms
noms = [fake.name() for _ in range(50)]  # 50 personnes

# Variables possibles
accompagnement_tuteur = ["Oui", "Non", "Partiellement"]
difficultes = ["Trop faciles", "Adaptées", "Trop difficiles"]
respect_deadlines = ["Toujours", "Souvent", "Rarement"]
temps_conciliation = ["Oui", "Non"]
anxiete_travail = ["Jamais", "Parfois", "Souvent"]
competences_necessaires = ["Oui", "Non"]
clarte_objectifs = ["Très clairs", "Assez clairs", "Peu clairs", "Pas du tout clairs"]

# Génération des données évolutives
data = []
for semaine in range(1, 20):  # 8 semaines
    for nom in noms:
        # 🔹 Dépendances logiques entre variables
        accompagnement = random.choice(accompagnement_tuteur)
        difficulté = random.choice(difficultes)
        deadlines = random.choice(respect_deadlines)
        conciliation = random.choice(temps_conciliation)
        competences = random.choice(competences_necessaires)
        clarte = random.choice(clarte_objectifs)

        # Niveau de stress plus réaliste
        base_stress = random.randint(3, 8)  # Stress de base entre 3 et 8
        if accompagnement == "Non":
            base_stress += 2  # Moins d'accompagnement = plus de stress
        if difficulté == "Trop difficiles":
            base_stress += 2
        if deadlines == "Rarement":
            base_stress += 1
        if conciliation == "Non":
            base_stress += 1
        stress = max(1, min(10, base_stress))

        # Intérêt des missions dépend de la clarté et des compétences requises
        base_interet = random.randint(2, 4)
        if clarte in ["Très clairs", "Assez clairs"]:
            base_interet += 1
        if competences == "Oui":
            base_interet += 1
        interet = max(1, min(5, base_interet))

        # Anxiété liée au stress et aux délais
        if stress > 7 or deadlines == "Rarement":
            anxiete = "Souvent"
        elif stress > 5:
            anxiete = "Parfois"
        else:
            anxiete = "Jamais"

        # Soutien équipe
        if accompagnement == "Oui":
            soutien = random.randint(4, 5)  # Bon soutien
        elif accompagnement == "Partiellement":
            soutien = random.randint(2, 4)
        else:
            soutien = random.randint(1, 3)  # Peu de soutien

        #Génération de remarques aléatoires
        remarque = fake.sentence(nb_words=10)

        # Ajout des données
        data.append([
            nom, stress, accompagnement, interet, difficulté, deadlines,
            conciliation, anxiete, soutien, competences, clarte, remarque, semaine
        ])

# Création du DataFrame
df = pd.DataFrame(data, columns=columns)

# Sauvegarde en CSV
file_path = "data/data_realistic.csv"
df.to_csv(file_path, index=False)
file_path
