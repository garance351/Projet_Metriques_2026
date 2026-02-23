import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :
@app.route("/contact")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"  

@app.route("/contact", methods=["GET", "POST"])
def MaPremiereAPI():
    # Si l'utilisateur a cliqué sur "Envoyer" (Méthode POST)
    if request.method == "POST":
        prenom = request.form.get("prenom")
        nom = request.form.get("nom")
        message = request.form.get("message")
#On ouvre un fichier (il sera créé automatiquement s'il n'existe pas)
        with open("messages.txt", "a", encoding="utf-8") as fichier:
            fichier.write(f"De: {prenom} {nom}\n")
            fichier.write(f"Message: {message}\n")
            fichier.write("-" * 30 + "\n")
#Message de confirmation basique affiché à l'écran
        return "Merci ! Votre message a bien été enregistré."

#Si l'utilisateur arrive simplement sur la page (Méthode GET)
        return render_template('contact.html')

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
