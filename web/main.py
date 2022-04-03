import flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import db
import operator

app = Flask(__name__)


@app.route('/')
def index():
    # getting top 5 keywords
    keywords = db.getTopKeywords()
    keywords_clear = []
    counter = {}

    for i in keywords:
        keywords_clear.append(i[0])

    for elem in keywords_clear:
        counter[elem] = counter.get(elem, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 1}
    sorted_d = list(dict(sorted(doubles.items(), key=operator.itemgetter(1), reverse=True)))[:5]

    # getting top languages
    lang = db.getTopLanguages()
    lang_clear = []
    counter_ = {}

    for i in lang:
        lang_clear.append(i[0])

    for elem in lang_clear:
        counter_[elem] = counter_.get(elem, 0) + 1

    doubles_ = {element: count for element, count in counter_.items() if count > 1}
    sorted_d_lang = list(dict(sorted(doubles_.items(), key=operator.itemgetter(1), reverse=True)))[:5]

    # getting semantic result
    semantic = db.getSemanticResults()
    semantic_clear = []
    counter_ = {}

    negative = 0
    positive = 0
    neutral = 0
    skip = 0

    for i in semantic:
        semantic_clear.append(i[0])

    for elem in semantic_clear:
        counter_[elem] = counter_.get(elem, 0) + 1

    doubles_ = {element: count for element, count in counter_.items() if count > 1}

    for key in doubles_:
        if key == 'negarive':
            negative = doubles_[key]
        if key == 'positive':
            positive = doubles_[key]
        if key == 'neutral':
            neutral = doubles_[key]
        if key == 'skip':
            skip = doubles_[key]

    return render_template('index.html', languages=sorted_d_lang, keyword=sorted_d, skip=skip, negative=negative,
                           positive=positive, neutral=neutral)
    # return str(sorted_d)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('Search.html', result=None)
    if request.method == 'POST':
        request_ = request.form['search']

        return redirect(f'/search/{request_}')

@app.route('/search/<query>')
def search_req(query):
    find = db.findNews(query)

    return render_template('Search.html', result=find)

if __name__ == '__main__':
    app.run(debug=True)
