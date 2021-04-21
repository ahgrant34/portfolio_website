from flask import Flask, render_template, request, url_for
import smtplib
import requests as req
from datetime import datetime
import markdown
import os

app = Flask(__name__)

# pulling in API data and reformatting

articles = req.get("https://ag-portfolio-strapi.herokuapp.com/articles").json()

#articles = req.get("http://localhost:1337/articles").json()

def date_formatter(articles):
    for article in articles:
        article['date_posted']= datetime.strptime(article['date_posted'], '%Y-%m-%d').strftime('%B %d, %Y')
        article['date_edited']= datetime.strptime(article['date_edited'], '%Y-%m-%d').strftime('%B %d, %Y')

def get_categories(article):
    categories = []
    for category in article['categories']:
        categories.append(category['name'])
    return categories


def get_all_categories(articles):
    categories = []
    for article in articles:
        for category in article['categories']:
            categories.append(category['name'])

    unique_categories = list(set(categories))
    return unique_categories

# Begin Routes

@app.route("/")

@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/aboutme")
def aboutme():
    return render_template("aboutme.html")

@app.route("/projects")
def projects():

    articles = req.get("https://ag-portfolio-strapi.herokuapp.com/articles").json()
    #articles = req.get("http://localhost:1337/articles").json()

    date_formatter(articles)

    categories = get_all_categories(articles)

    return render_template("projects.html", articles=articles, categories=categories)

@app.route("/resume")
def resume():

    return render_template("resume.html")

@app.route("/test")
def test():

    return render_template("test.html")

@app.route("/project/<int:num>")
def project(num):

    articles = req.get("https://ag-portfolio-strapi.herokuapp.com/articles").json()
    #articles = req.get("http://localhost:1337/articles").json()

    date_formatter(articles)

    for article in articles:
        if article['id'] == num:
            title = article['title']
            description = article['description']
            github_link= article['github_link']
            author = article['author']
            content = markdown.markdown(article['content'])
            date_posted = article['date_posted']
            date_edited = article['date_edited']
            categories = get_categories(article)
            article_banner_url = article['article_banner']



    return render_template("article.html", title=title, description=description, github_link=github_link,
                           author=author, content=content, date_posted=date_posted, date_edited=date_edited,
                           categories=categories, article_banner_url=article_banner_url)


@app.route("/contactinfo")
def contactinfo():
    return render_template("contactinfo.html")

@app.route("/form", methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    message = request.form.get("message")

    #email_message= "".join(["Name ", first_name," ", last_name,"\nEmail Address ",email,
                          # "\nThis person has reached out with the following message \n", message])

    email_message = "\nName: {} {} \n\nEmail Address: {} \n\nThis person has reached out with the following message: " \
                    "\n\n{}".format(first_name, last_name, email, message)

    email_message= str(email_message)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("andrewhansgrantwebsite@gmail.com", os.environ[email_password])
    server.sendmail("andrewhansgrantwebsite@gmail.com", "andrewhansgrant@gmail.com", email_message)

    return render_template("form.html", first_name=first_name, last_name=last_name, email=email, message=message, email_message=email_message)


if __name__ == "__main__":
    app.run(debug=True)
