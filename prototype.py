from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello(user):
    return render_template

@app.route("/list/<letter>")
def show_list_by_letter(letter):
    html = requests.get("http://mejortorrent.com/series-letra-%s.html" % letter)
    soup = BeautifulSoup(html.content)
    series = {}
    for link in soup.findAll('a'):
        if str(link.get('href'))[1:8] == 'serie-d':
            series[link.contents[0]] = link.get('href')
    
    return render_template('letter.html',
                           series=series,
                           letter=letter,
                           section="Series - letra %s" % letter)

if __name__ == "__main__":
    app.run(debug=True)
