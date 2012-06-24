from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/<user>")
def hello(user):
    return "Hello World! Is %s your name?" % user

@app.route("/list/<letter>")
def show_list_by_letter(letter):
    html = requests.get("http://mejortorrent.com/series-letra-%s.html" % letter)
    soup = BeautifulSoup(html.content)
    for link in soup.findAll('a'):
        print link.get('href')
    return "done"

if __name__ == "__main__":
    app.run(debug=True)
