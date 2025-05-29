from flask import Flask, request, jsonify
from gnews import GNews
from newspaper import Article

app = Flask(__name__)
google_news = GNews(language='portuguese', country='Brazil', max_results=5)

def extrair_detalhes(url):
    try:
        article = Article(url, language='pt')
        article.download()
        article.parse()
        article.nlp()
        return {
            "texto": article.text,
            "resumo": article.summary
        }
    except Exception as e:
        return {
            "texto": "",
            "resumo": "",
            "erro": str(e)
        }

@app.route('/noticias-completas', methods=['GET'])
def noticias_completas():
    termo = request.args.get('termo', '')
    if not termo:
        return jsonify({'erro': 'Informe um termo de busca (?termo=...)'}), 400

    resultados = google_news.get_news(termo)
    noticias = []
    for r in resultados:
        detalhes = extrair_detalhes(r.get('url'))
        noticias.append({
            "titulo": r.get('title'),
            "descricao": r.get('description'),
            "link": r.get('url'),
            "data": r.get('published date'),
            "texto": detalhes.get("texto"),
            "resumo": detalhes.get("resumo")
        })
    return jsonify(noticias)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
