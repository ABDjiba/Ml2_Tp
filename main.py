from fastapi import FastAPI
import uvicorn
import pandas as pd

app = FastAPI()
@app.get("/jointure")
async def jointure():

    impressions=pd.read_csv("https://raw.githubusercontent.com/ABDjiba/ML2/main/impressions.csv")

    clics=pd.read_csv("https://raw.githubusercontent.com/ABDjiba/ML2/main/clics.csv")

    achats=pd.read_csv("https://raw.githubusercontent.com/ABDjiba/ML2/main/achats.csv")


    resultat1 = pd.merge(impressions, clics, on="cookie_id", how="left")
    resultat = pd.merge(resultat1, achats, on="cookie_id", how="left")

    resultat=resultat.fillna("-")

    return resultat.to_dict(orient="records")







