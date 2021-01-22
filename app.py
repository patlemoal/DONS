from flask import Flask, render_template, request
from pymongo import MongoClient
import json


#connection à Mongo Atlas

client = MongoClient("mongodb+srv://patricia:123@cluster0.gd0dm.mongodb.net/?retryWrites=true&w=majority")

#base de données : projet-don, table : simon
my_collection = client.projet_don.simon


app = Flask(__name__)
# app fait appel au gestionnaire qui utilise flask (équivalant de my db); méthode comme le init dans les classes

#CONNECTION A LA PAGE D'ACCEUIL (page)
@app.route('/')
def page():
    return render_template('page.html')


#CONNECTION AU FORMULAIRE
@app.route('/formulaire')
def formulaire():
    return render_template("formulaire.html")

#on lie cette fonction au formulaire htlm , cette fonction sera appellee lorsque lé formulaire sera validé
#requete pour envoyer les informations saisies dans le formulaire vers la base de données (et on converti les données en dons en format numérique)
@app.route('/resultatduformulaire', methods =['GET',"POST"])#methods POST consiste à envoyer des données, get recoit les données du formulaire
def resultatduformulaire():
    data = request.form.to_dict()
    data['don'] = int(data['don'])
    my_collection.insert_one(data)

    return render_template('page.html')  
    

@app.route('/afficherlesdons')
def afficherlesdons():
    
    # On récupère les données de la base de données
    #on déclare un tableau pour récuperer les données de la bbd
    resultat = []
    #on cree une variable qui récupère le total des dons
    don = 0
    #curseur que l on déplace
    curseur = my_collection.find()
    #obj est une ligne lue 
    #next nouvel élément
    obj = next(curseur, None)
    
    # Tant que obj n'est pas vide
    while obj:
        # On ajoute la ligne lu à notre variable
        resultat.append(obj)
        #on ajoute tous les dons 
        don += obj['don']
        #on lit la ligne suivante
        obj = next(curseur, None)
    #fonction pour afficher le format correct des nombres
    
    don = "{:,}".format(don).replace(","," ")
    return render_template("consultation.html", resultat = resultat, don_count = don)


if __name__ == "__main__" :
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(port=8000, debug=True)