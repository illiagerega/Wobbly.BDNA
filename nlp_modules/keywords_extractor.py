from multi_rake import Rake
import db

texts = db.selectAllTexts()

for text in texts:
    rake = Rake()
    keywords = rake.apply(text[3])

    for words in keywords[15:20]:
        result = db.checkKeywords(text[1], text[0])[0]
        if result != 1:
            db.insertKeywords(text[1], text[0], words[0])
        else:
            continue
