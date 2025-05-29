from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/noticias', methods=['GET'])
def get_noticias():
    termo = request.args.get('termo', '')  # parâmetro para busca
    url = f'https://news.google.com/search?q={termo}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    noticias = []
    for item in soup.select('article'):
        titulo = item.select_one('h3, h4')
        if not titulo:
            continue
        titulo = titulo.text
        link_tag = item.find('a', href=True)
        link = f"https://news.google.com{link_tag['href'][1:]}" if link_tag else ''
        resumo = item.select_one('.HO8did').text if item.select_one('.HO8did') else ''
        data = item.select_one('time')
        data_pub = data['datetime'] if data and data.has_attr('datetime') else ''
        noticias.append({
            'titulo': titulo,
            'resumo': resumo,
            'data': data_pub,
            'link': link
        })
    return jsonify(noticias)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
