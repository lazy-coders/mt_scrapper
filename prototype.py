from flask import Flask
from flask import request
from flask import render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html',
                           section="Prototype - Inicio")


@app.route('/serie/list/<letter>')
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


@app.route('/serie/url', methods=['GET'])
def show_chapters():
    # Controlar la peticion
    url = request.args.get('url', '')
    html = requests.get("http://mejortorrent.com%s" % url)
    soup = BeautifulSoup(html.content)
    episodios = {}

    for image in soup.findAll('img'):
        if str(image.get('src'))[0:52] == 'http://www.mejortorrent.com/uploads/imagenes/series/':
            cover = image.get('src')

    for input in soup.findAll('input'):
        if str(input.get('name'))[0:9] == 'episodios':
            episodios[input.get('name')] = input.get('value')

    # Generamos la peticion POST y parseamos los torrents

    payload = {'checkall': 'on', 'total_capis': len(episodios), 'tabla': 'series'}
    payload = dict(payload.items() + episodios.items())
    post = requests.post('http://mejortorrent.com/secciones.php?sec=descargas&ap=contar_varios', payload)
    soup_post = BeautifulSoup(post.text)

    torrents = []

    for link in soup_post.findAll('a'):
        if str(link.get('href'))[0:52] == 'http://www.mejortorrent.com/uploads/torrents/series/':
            torrents.append(link.get('href'))

    return render_template('serie.html', section=request.args.get('name', ''),
                           torrents=torrents,
                           cover=cover)
        

if __name__ == "__main__":
    app.run(debug=True)
