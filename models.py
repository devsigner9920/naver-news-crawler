class NewsArticle:
    def __init__(self, title, link, description, press, article_time):
        self.title = title
        self.link = link
        self.description = description
        self.press = press
        self.article_time = article_time

    def to_dict(self):
        return {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "press": self.press,
            "article_time": self.article_time
        }
