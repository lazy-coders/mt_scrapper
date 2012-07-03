from flask import Flask, request, render_template
import string
import requests
import urllib2
import os
from bs4 import BeautifulSoup


def downloadFile(url, directory):
    fileName = url[url.rfind('/')+1:len(url)]
    # To avoid errors due special characters in the filename,
    # we use urllib2 to quote it
    url = url[0:url.rfind('/')+1] + urllib2.quote(fileName)
    fileName = os.path.join(directory, fileName)

    file = urllib2.urlopen(url)
    localFile = open(fileName, 'w')
    localFile.write(file.read())
    localFile.close()


app = Flask(__name__)
app.config.from_pyfile("myconf.py")

@app.route("/")
def hello():
    return render_template('home.html',
                           section="Prototype - Inicio",
                           string=string)


@app.route('/serie/list/<letter>')
def show_list_by_letter(letter):
    html = requests.get("http://mejortorrent.com/series-letra-%s.html" % letter)
    soup = BeautifulSoup(html.content)
    series = {}
    for link in soup.findAll('a'):
        if str(link.get('href'))[1:8] == 'serie-d':
            series[link.contents[0]] = link.get('href')

    return render_template('letter.html',
                           indices=sorted(series),
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

    for torrent in torrents:
        downloadFile(torrent, app.config['DOWNLOAD_DIR'])

    return render_template('serie.html', section=request.args.get('name', ''),
                           torrents=torrents,
                           cover=cover)


if __name__ == "__main__":
    app.run(debug=True)
