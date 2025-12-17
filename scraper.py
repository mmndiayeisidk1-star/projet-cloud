import requests
from bs4 
import BeautifulSoup
import csv
from datetime import datetime
import boto3

URL = "https://immobilier-au-senegal.com/terrains-a-vendre/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

annonces = soup.find_all("h3")

print(f"Number of annonces: {len(annonces)}")
if not annonces:
    print("No annonces found. First 1000 chars of HTML:")
    print(soup.prettify()[:1000])

filename = f"annonces_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["Titre", "Prix", "Localisation"])

    for annonce in annonces:
        titre = annonce.find("a").text.strip() if annonce.find("a") else "N/A"
        location_p = annonce.find_next("p")
        if location_p:
            localisation = location_p.find("a").text.strip() if location_p.find("a") else "N/A"
        else:
            localisation = "N/A"
        price_p = location_p.find_next("p") if location_p else None
        if price_p:
            prix = price_p.text.strip()
        else:
            prix = "N/A"

        writer.writerow([titre, prix, localisation])

print(f"Fichier {filename} généré avec succès")



def upload_file_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_name)

file_path = "data/annnonces.csv"
file_name = "annnonces.csv"
MY_BUCKET_NAME = "m2dsia-ndiaye-mmoustapha"
upload_file_s3(file_path, MY_BUCKET_NAME, file_name)
