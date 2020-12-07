import pandas as pd
import joblib 
import pymysql
import time
import datetime
from pymysql.cursors import DictCursor
from string import digits, ascii_letters, ascii_lowercase, ascii_uppercase, punctuation

def num_count(data):
    return len([i for i in data if i in digits])


def symb_count(data):
    return len([i for i in data if i in punctuation])


def letter_count(data):
    return len([i for i in data if i in ascii_letters])


def lower_count(data):
    return len([i for i in data if i in ascii_letters and i in ascii_lowercase])


def upper_count(data):
    return len([i for i in data if i in ascii_letters and i in ascii_uppercase])


def vowel_count(data):
    return len([i for i in data if i in ascii_letters and i in 'eyuioa'])


def consonant_count(data):
    return len([i for i in data if i in ascii_letters and i not in 'eyuioa'])


def prepare_data(data):
    data['password'] = data['password'].astype(str)
    prepared = pd.DataFrame()
    prepared['len'] = data['password'].str.len()
    prepared['num_count'] = data['password'].apply(num_count)
    prepared['symb_count'] = data['password'].apply(symb_count)
    prepared['letter_count'] = data['password'].apply(letter_count)
    prepared['lower_count'] = data['password'].apply(lower_count)
    prepared['upper_count'] = data['password'].apply(upper_count)
    prepared['vowel_count'] = data['password'].apply(vowel_count)
    prepared['consonant_count'] = data['password'].apply(consonant_count)
    return prepared


def predict(password):
    password = prepare_data(pd.DataFrame([[password]], columns=['password']))
    return clf.predict(password)[0]

if __name__ == "__main__":
    clf = joblib.load('rf-classifier.pkl')

    try:
        connection = pymysql.connect(
            host = '172.17.0.2',
            port = 3306,
            user = 'root',
            password = 'nimda',
            db = 'password_db',
            autocommit = True,
            cursorclass = DictCursor
        )
    except pymysql.err.OperationalError as err:
        raise SystemExit(err)
    
    with connection.cursor() as cursor:
        query = "select * from password where category is null"
        while True:
            try:
                cursor.execute(query)
                print(datetime.datetime.now(), "=== Сделан запрос =>", query, "\n Получено строк =>", str(cursor.rowcount))
            except (pymysql.err.ProgrammingError, pymysql.err.OperationalError) as err:
                print(err)
            else:
                rows = cursor.fetchall()
                for row in rows:
                    upd_query = "update password set category = " + str(predict(row['password'])) + " where password = '" + row['password'] + "'"
                    try:
                        cursor.execute(upd_query)
                        print(datetime.datetime.now(), "=== Сделан запрос =>", upd_query)
                    except (pymysql.err.ProgrammingError, pymysql.err.OperationalError) as err:
                        print(err)
            time.sleep(1)  
    # connection.close()
