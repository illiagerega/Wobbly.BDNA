import db
from langdetect import detect

texts = db.selectAllTexts()

for text in texts:
    checkText = db.findLangLink(text[0])[0]

    if checkText != 1:
        try:
            lang = detect(text[3])
            db.insertLangLink(text[1], text[0], lang)
        except:
            db.insertLangLink(text[1], text[0], 'None')
    else:
        continue
