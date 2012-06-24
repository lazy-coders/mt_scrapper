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

    # Hay que crear una peticion POST con los valores del dict episodios
    # checkall=on, total_capis=dict.count y tabla=series contra la url
    # http://mejortorrent.com/secciones.php?sec=descargas&ap=contar_varios

    for e, v in episodios.items():
        print "Ep %s: %s" % (e, v)

    return "<h1>Imagen</h1><img src=\"%s\" />" % cover
        

if __name__ == "__main__":
    app.run(debug=True)
