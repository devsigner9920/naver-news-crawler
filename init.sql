CREATE TABLE news_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    link VARCHAR(255),
    description TEXT,
    press VARCHAR(100),
    article_time DATETIME
);