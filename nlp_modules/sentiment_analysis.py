import db
import operator
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

texts = db.selectAllTexts()

for i in texts:
    text = i[3]
    text = text.split()

    array_5 = [' '.join(text[i:i + 5]) for i in range(0, len(text), 5)]
    array_7 = [' '.join(text[i:i + 7]) for i in range(0, len(text), 7)]

    chars = []
    counter = {}

    results = model.predict(array_5, k=2)
    for message, sentiment in zip(array_5, results):
        for key in sentiment:
            if key == 'skip':
                continue
            else:
                chars.append(key)

    results = model.predict(array_7, k=2)
    for message, sentiment in zip(array_7, results):
        for key in sentiment:
            if key == 'skip':
                continue
            else:
                chars.append(key)

    for elem in chars:
        counter[elem] = counter.get(elem, 0) + 1

    doubles = {element: count for element, count in counter.items() if count > 1}
    sorted_d = dict(sorted(doubles.items(), key=operator.itemgetter(1), reverse=True))

    try:
        if sorted_d['negative'] >= 100:
            print('negative')
            result = db.checkSemantic(i[1], i[0])
            if result != 1:
                db.insertSemantic(i[1], i[0], 'negative')
                continue
            else:
                continue
    except:
        print('neutral')
        result = db.checkSemantic(i[1], i[0])
        if result != 1:
            db.insertSemantic(i[1], i[0], 'neutral')
        else:
            continue

    try:
        if sorted_d['positive'] >= 40:
            print('positive')
            result = db.checkSemantic(i[1], i[0])
            if result != 1:
                db.insertSemantic(i[1], i[0], 'positive')
                continue
            else:
                continue
    except:
        print('neutral')
        result = db.checkSemantic(i[1], i[0])
        if result != 1:
            db.insertSemantic(i[1], i[0], 'neutral')
        else:
            continue

    print('neutral')
    result = db.checkSemantic(i[1], i[0])
    if result != 1:
        db.insertSemantic(i[1], i[0], 'neutral')
    else:
        continue



