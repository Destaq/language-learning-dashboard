# load the data/chengyu.json file into the postgresql:///ll_dashboard database

import json
import os
import dotenv
import psycopg2

# load dotenv
dotenv.load_dotenv()

# load in the file as a csv
with open('data/chengyu.json') as f:
    data = json.load(f)

# connect to the database
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

# the format of chengyu.json is a list of dictionaries
# example
# {"derivation": "语出《法华经·法师功德品》下至阿鼻地狱。”", "example": "但也有少数意志薄弱的……逐步上当，终至堕入～。★《上饶集中营·炼狱杂记》", "explanation": "阿鼻梵语的译音，意译为无间”，即痛苦无有间断之意。常用来比喻黑暗的社会和严酷的牢狱。又比喻无法摆脱的极其痛苦的境地。", "pinyin": "ā bí dì yù", "word": "阿鼻地狱", "abbreviation": "abdy"}

# loop through the list of dictionaries and add them to the chengyu table in the database
for i in data:
    word = i['word']
    pinyin = i['pinyin']
    abbreviation = i['abbreviation']
    explanation = i['explanation']
    example = i['example']
    derivation = i['derivation']
    cur.execute("INSERT INTO chengyu(word, pinyin, abbreviation, explanation, example, derivation) VALUES (%s, %s, %s, %s, %s, %s)", (word, pinyin, abbreviation, explanation, example, derivation))

conn.commit()
conn.close()
