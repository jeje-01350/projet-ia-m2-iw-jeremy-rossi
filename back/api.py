from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import uvicorn
import numpy as np
import pandas as pd

# Initialisation de l'application FastAPI
app = FastAPI()

# Définition des modèles de données d'entrée
class DonneesPredictionNote(BaseModel):
    localisation: str
    superficie: float
    cout: float

class DonneesPredictionAnnee(BaseModel):
    localisation: str

class DonneesPredictionGarage(BaseModel):
    localisation: str
    cout: float

# Initialisation des modèles de machine learning
modele_note = LinearRegression()
modele_annee = LinearRegression()
modele_garage = LogisticRegression(max_iter=200)

# Utilisation cohérente de l'encodeur
encodeur_labels = LabelEncoder()

# Variable pour vérifier si les modèles sont entraînés
modeles_entraines = False

# Endpoint pour entraîner les modèles
@app.post("/entrainement")
async def entrainement():
    global modeles_entraines
    global modele_note, modele_annee, modele_garage
    global encodeur_labels

    # Lire le fichier CSV
    donnees = pd.read_csv('suites.csv')

    # Encoder la colonne 'localisation'
    donnees['localisation_codee'] = encodeur_labels.fit_transform(donnees['ville'])

    # 1. Régression linéaire pour prédire la note
    X_note = donnees[['localisation_codee', 'surface', 'price']]
    y_note = donnees['note']
    modele_note.fit(X_note, y_note)

    # 2. Régression linéaire pour prédire l'année de construction
    X_annee = donnees[['localisation_codee']]
    y_annee = donnees['annee']
    modele_annee.fit(X_annee, y_annee)

    # 3. Classification logistique pour prédire la présence d'un garage
    X_garage = donnees[['localisation_codee', 'price']]
    y_garage = donnees['garage']
    modele_garage.fit(X_garage, y_garage)

    # Marquer les modèles comme entraînés
    modeles_entraines = True

    return {"message": "Modèles entraînés avec succès."}

# Endpoint pour prédire la note en fonction de la localisation, superficie et coût
@app.post("/prediction-note")
async def prediction_note(data: DonneesPredictionNote):
    if not modeles_entraines:
        raise HTTPException(status_code=400, detail="Le modèle n'est pas encore entraîné.")

    # Encoder la localisation
    localisation_codee = encodeur_labels.transform([data.localisation])[0]
    X_nouvelle = np.array([[localisation_codee, data.superficie, data.cout]])

    note_predite = modele_note.predict(X_nouvelle)[0]
    return {"note_predite": note_predite}

# Endpoint pour prédire l'année en fonction de la localisation et calculer R² et RMSE
@app.post("/prediction-annee")
async def prediction_annee(data: DonneesPredictionAnnee):
    if not modeles_entraines:
        raise HTTPException(status_code=400, detail="Le modèle n'est pas encore entraîné.")

    # Encoder la localisation pour la nouvelle donnée
    localisation_codee = encodeur_labels.transform([data.localisation])[0]
    X_nouvelle = np.array([[localisation_codee]])

    annee_predite = modele_annee.predict(X_nouvelle)[0]

    # Lire le fichier CSV
    donnees = pd.read_csv('suites.csv')

    # Encoder la colonne 'localisation' pour toutes les données
    donnees['localisation_codee'] = encodeur_labels.transform(donnees['ville'])

    # Calcul de R² et RMSE
    X_annee_all = donnees[['localisation_codee']]  # Assurez-vous que c'est un DataFrame à deux dimensions
    y_annee_all = donnees['annee']
    y_pred_all = modele_annee.predict(X_annee_all)
    r2 = modele_annee.score(X_annee_all, y_annee_all)
    rmse = np.sqrt(mean_squared_error(y_annee_all, y_pred_all))

    return {"annee_predite": annee_predite, "R²": r2, "RMSE": rmse}

# Endpoint pour prédire la présence d'un garage en fonction du coût et de la localisation
@app.post("/prediction-garage")
async def prediction_garage(data: DonneesPredictionGarage):
    if not modeles_entraines:
        raise HTTPException(status_code=400, detail="Le modèle n'est pas encore entraîné.")

    # Encoder la localisation
    localisation_codee = encodeur_labels.transform([data.localisation])[0]
    X_nouvelle = np.array([[localisation_codee, data.cout]])

    garage_predite = modele_garage.predict(X_nouvelle)[0]
    return {"garage_predite": bool(garage_predite)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
