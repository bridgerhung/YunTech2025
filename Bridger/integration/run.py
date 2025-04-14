from decodeJson import decodeJson
from keywords import keywords


decoder =decodeJson()
review =decoder.readFile()

keywordGetter =keywords()
print(keywordGetter.extract_keywords("Iphone16", modelMode =True))