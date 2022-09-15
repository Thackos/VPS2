# fonction qui recupere les articles
from pyVinted import Vinted
from urllib import request
import json

NB_ARTICLES = 1


def get_products(URL, nb):
    vinted = Vinted()
    items = vinted.items.search(URL, nb, 1)
    for item in items:
        print(item.title, ":", item.price + "€", ":", item.url)
    return items


def articles_to_json(art):
    obj1 = str(art[0].__dict__)
    new = obj1.replace("\'", "\"")
    new = new.replace("None", '0')
    new = new.replace("False", '0')
    new = new.replace("True", '1')
    new = new.replace("datetime.datetime(", '[')
    new = new.replace("), \"raw_timestamp\":", '], \"raw_timestamp\":')
    new = new.replace("tzinfo=datetime.timezone.utc", '0')
    new = new.replace('»', ' ')
    new = new.replace('«', ' ')
    new = new.replace("Levi's", 'Levis')
    new = new.replace("Jean's", 'Jean')

    # écrire dans le data.json
    jsonFile = open("data.json", "w")
    jsonFile.write(new)
    jsonFile.close()


# filtre les données utiles à envoyer
def filtre_json():
    with open('data.json') as mon_fichier:
        data = json.load(mon_fichier)
        # check if article is new
        mon_id = data["raw_data"]["id"]

        file = open("dataexist.txt", "r")
        if str(mon_id) in file.read():
            print("----> Article deja existant")
        else:
            with open('dataexist.txt', 'a') as file2:
                file2.write(str(mon_id) + "\n")
                new_data = data["raw_data"]["title"], data["raw_data"]["price"] + "€", data["raw_data"]["url"]
                return new_data


def envoie_discord(URL_VETEMENT, WEBHOOK_URL):
    articles = get_products(URL_VETEMENT, NB_ARTICLES)
    # création de la liste d'articles json a partir des articles -> data.json
    articles_to_json(articles)
    article_envoi = str(filtre_json())
    if article_envoi != 'None':
        # donnees utiles pour envoi sur discord
        payload = {
            'embeds': [
                {
                    'title': articles[0].title,
                    'description': "📏 | Taille: " + articles[0].size_title + \
                                   "\n\n" + \
                                   "💶 | Prix: " + articles[0].price + "€\n",
                    'url': articles[0].url,
                    "image": {
                        "url": articles[0].photo
                    },
                    'author': {'name': 'Premium Vinted Bot', 'icon_url': 'https://img1.freepng.fr/20180320/fbe/kisspng-computer-icons-social-media-robot-scalable-vector-drawing-vector-robot-5ab16e73a00f11.3357462015215775876556.jpg'},
                },
            ],
        }
        headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        }
        req = request.Request(url=WEBHOOK_URL,
                              data=json.dumps(payload).encode('utf-8'),
                              headers=headers,
                              method='POST')
        # envoyer la request a discord
        request.urlopen(req)
        print("Article envoyé")
