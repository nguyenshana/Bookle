import flask
from app_folder import app
from flask import render_template
from flask import redirect
from flask import flash, url_for
from flask import request
from wtforms import ValidationError

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from .forms import SearchForm



@app.route("/", methods = ['GET', 'POST'])
def index():
	form = SearchForm()
	if form.validate_on_submit():
		return redirect('/'+form.bookName.data)
	return render_template('index.html', form=form)


@app.route("/<bookSearch>", methods=['GET', 'POST'])
def bookPage(bookSearch):

	form = SearchForm()
	if form.validate_on_submit():
		return redirect('/'+form.bookName.data)

	book = urllib.parse.quote_plus(bookSearch)
	with urllib.request.urlopen("https://www.goodreads.com/search/index.xml?key=LFqpcgVHv19X8KCDzkQ9pw&q=" + book) as response:
		html = response.read()
	xml = ET.fromstring(html)
	booksPath = xml.find('search').find('results')
	title = [len(booksPath)]
	author = [len(booksPath)]
	authorURL = [len(booksPath)]
	image = [len(booksPath)]
	epublink = [len(booksPath)]
	openliblink = [len(booksPath)]
	sjpllink = [len(booksPath)]
	googlebookslink = [len(booksPath)]

	i = 0
	for b in booksPath:
		bookPath = b.find('best_book')
		title.append(str(bookPath.find('title').text))
		author.append(str(bookPath.find('author').find('name').text))
		authorParse = urllib.parse.quote_plus(str(author[i+1]))
		authorURL.append("https://www.goodreads.com/book/author/" + authorParse)
		image.append(str(bookPath.find('image_url').text))

		titleURL = urllib.parse.quote_plus(str(title[i+1]))
		epublink.append("https://www.epublink.com/?s=" + titleURL + "&post_type=product")

		openliblink.append("https://openlibrary.org/search?q=" + titleURL + "&mode=ebooks&has_fulltext=true")

		sjpllink.append("https://sjpl.bibliocommons.com/v2/search?query=" + titleURL + "&searchType=smart")

		googlebookslink.append("https://play.google.com/store/search?c=books&q=" + titleURL)

		i = i + 1


	return render_template('bookPage.html', form=form, title=title, author=author, authorURL=authorURL, image_url=image, epublink=epublink, openliblink=openliblink, sjpllink=sjpllink, googlebookslink=googlebookslink)


