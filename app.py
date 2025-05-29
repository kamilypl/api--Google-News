from flask import Flask, request, jsonify
from gnews import GNews

app = Flask(__name__)
google_news = GNews(language='portuguese', country='Brazil', max_results=10)  # Configurações clássicas

@app.route('/noticias', methods=['GET'])
def noticias():
    termo = request.args.get('termo', '')
    if not termo:
        return jsonify({'erro': 'Informe um termo de busca com o parâmetro ?termo=...'}), 400

    # Busca as notícias pelo termo
    results = google_news.get_news(termo)
    # Ajusta formato do retorno (apenas campos relevantes)
    noticias = [
        {
            "titulo": r.get('title'),
            "descricao": r.get('description'),
            "link": r.get('url'),
            "data": r.get('published date')
        }
        for r in results
    ]
    return jsonify(noticias)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
