from old.annonceRepository import AnnonceRepository
import requests
import re

def contact(annonce_id, email, msg, name, phone) -> requests.Response:
    s = requests.Session()

    s.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    })
    
    payload = {
        "email": email,
        "listingId": annonce_id,
        "listingPublicationId": 1,
        "message": msg,
        "name": name,
        "phone": phone
    }

    res = s.post("https://www.seloger.com/annoncesbff/2/Contact", json=payload)
    return res


def extract_annonce_id_from_url(url: str) -> int:
    extract_id_pattern = r"/(\d+)\.htm"
    match = re.search(pattern=extract_id_pattern, string=url)
    if match:
        number = int(match.group(1))
        return number
    return -1

def contact_agencies(urls: list[str], repository: AnnonceRepository, email: str, name: str, phone: str) -> None:

    contact_message = "Bonjour, je suis intéressé par cet appartement ! Prenez-vous actuellement des rendez-vous pour des visites ? Si oui, je suis intéressé. Je peux vous envoyer mon dossier par mail, et suis joignable au 0760912574. Vous pouvez également trouver mon dossier sur le site du gouvernement 'DossierFacile.fr' à cette adresse: https://locataire.dossierfacile.fr/file/b04472cd-9577-4115-a88f-22daa1a6ea30 . Bonne journée !"

    for url in urls:
        id = extract_annonce_id_from_url(url)
        if not repository.annonce_exists(id):
            trySend = contact(id, email, contact_message, name, phone)
            if trySend.status_code == 200:
                print(f"contacted annonce: {id}  --> {url}")
                #print(trySend.content)
                repository.save_annonce(id, url)
        else:
            print(f"annonce: {id} already treated")
