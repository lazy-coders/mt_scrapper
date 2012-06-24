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
    series = {}
    for link in soup.findAll('a'):
        if str(link.get('href'))[1:8] == 'serie-d':
            series[link.contents[0]] = link.get('href')
    
    for serie, link in series.iteritems():
        print "%s: %s" % (serie, link)

    return "done"

if __name__ == "__main__":
    app.run(debug=True)
