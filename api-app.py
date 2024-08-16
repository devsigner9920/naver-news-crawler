from flask import Flask, jsonify, json, Response

from db import with_db_connection
from models import NewsArticle

app = Flask(__name__)


@app.route('/news', methods=['GET'])
@with_db_connection
def get_news_articles(connection):
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM news_articles"
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    articles = [NewsArticle(
        title=row['title'],
        link=row['link'],
        description=row['description'],
        press=row['press'],
        article_time=row['article_time']
    ) for row in rows]

    articles_dict = [article.to_dict() for article in articles]
    response = json.dumps(articles_dict, ensure_ascii=False)

    return Response(response, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
