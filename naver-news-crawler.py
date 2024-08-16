import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
from models import NewsArticle
from db import with_db_connection  # 데코레이터 가져오기


# 뉴스 기사를 스크랩하고 데이터베이스에 저장하는 함수
@with_db_connection
def fetch_and_store_news_articles(connection):
    cursor = connection.cursor()

    url = 'https://news.naver.com/breakingnews/section/105/283'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    timezone = pytz.timezone('Asia/Seoul')
    now = datetime.now(timezone)

    news_list = soup.select('div.sa_item_flex')
    news_articles = []

    for news in news_list:
        link = news.select_one('a.sa_thumb_link')['href']
        title = news.select_one('a.sa_text_title').get_text(strip=True)
        description = news.select_one('div.sa_text_lede').get_text(strip=True)
        press = news.select_one('div.sa_text_press').get_text(strip=True)
        time_text = news.select_one('div.sa_text_datetime b').get_text(strip=True)

        # 시간 계산
        datetime_obj = now
        if '시간전' in time_text:
            hours_ago = int(time_text.replace('시간전', '').strip())
            datetime_obj = now - timedelta(hours=hours_ago)
        elif '분전' in time_text:
            minutes_ago = int(time_text.replace('분전', '').strip())
            datetime_obj = now - timedelta(minutes=minutes_ago)
        elif '일전' in time_text:
            days_ago = int(time_text.replace('일전', '').strip())
            datetime_obj = now - timedelta(days=days_ago)

        datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

        # NewsArticle 객체 생성
        article = NewsArticle(
            title=title,
            link=link,
            description=description,
            press=press,
            article_time=datetime_str
        )
        news_articles.append(article)

    # 뉴스 기사를 시간순으로 정렬
    news_articles = sorted(news_articles, key=lambda x: x.article_time)

    # 데이터베이스에 삽입
    insert_query = """
        INSERT INTO news_articles (title, link, description, press, article_time)
        VALUES (%s, %s, %s, %s, %s)
    """

    for article in news_articles:
        print(article.title, article.link, article.description, article.press, article.article_time)
        cursor.execute(insert_query,
                       (article.title, article.link, article.description, article.press, article.article_time))

    connection.commit()
    cursor.close()


# 뉴스 기사 스크랩 및 저장 실행
fetch_and_store_news_articles()