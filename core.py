from xml.etree.ElementTree import fromstring
from collections import defaultdict
import builtins
import sqlite3
import requests
import configparser
import os

# import datetime
#from datetime import date, timedelta

def get_autorization():
    """ Get Stone Token"""
    config = configparser.ConfigParser()
    config.read('config.txt', encoding="utf-8")
    autorization = config.get('configuration', 'authorization')
    return autorization

def get_stone_report(report_date):
    """ Get Stone XML """

    url = 'https://conciliation.stone.com.br/conciliation-file/v2/{}'.format(report_date) #report_date.strftime('%Y%m%d'))
    headers = {
        "Authorization":get_autorization(),
        # "Accept-Encoding": "gzip"
    }
    r = requests.get(url, headers=headers)
    return r.text

def get_gross_amount(tree):
    """ Parse Gross Amount """
    r = []
    for item in tree.findall("FinancialTransactions"):
        for x in item.findall('Transaction'):
            for y in x.findall('Installments'):
                for k in y.findall('Installment'):
                    bruto = k.find('GrossAmount')
                    r.append(float(bruto.text))
    return (sum(r))

def get_net_amount(tree):
    """ Parse Net Amount """
    r = []
    for item in tree.findall("FinancialTransactions"):
        for x in item.findall('Transaction'):
            for y in x.findall('Installments'):
                for k in y.findall('Installment'):
                    bruto = k.find('NetAmount')
                    r.append(float(bruto.text))
    return (sum(r))

def get_prevision(tree):
    """ Paser Prevision Dates """
    l_net_amount = []
    l_prevision_date = []
    for item in tree.findall("FinancialTransactions"):
        for x in item.findall('Transaction'):
            for y in x.findall('Installments'):
                for k in y.findall('Installment'):
                    v_net_amount = k.find('NetAmount')
                    v_prevision_date = k.find('PrevisionPaymentDate')
                    l_net_amount.append(float(v_net_amount.text))
                    date = v_prevision_date.text
                    date = date[6:8] + "/" + date[4:6] + "/" + date[0:4]
                    l_prevision_date.append(date)
    r = list(zip(l_prevision_date, l_net_amount))
    d = defaultdict(list)
    for k, v in r:
        d[k].append(v)
    return (d)

def table_create():
    #check if database exists if not create it.

    if os.path.exists("DataStone.db"):
        return None

    #connect database
    database = sqlite3.connect("DataStone.db")

    #cursor object
    cursor = database.cursor()

    #Create Table

    cursor.execute(""" 
    CREATE TABLE DataStone (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            report_date DATE NOT NULL,
            date DATE NOT NULL,
            value FLOAT
    );
    """)

    print("Tabela Criada com Sucesso")

    database.close()

def insert_data(report_date, date, value):
    """ Insert data in DataStone.db """
    conn = sqlite3.connect('DataStone.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DataStone (report_date, date, value) VALUES (?, ?, ?)", (report_date, date, value))
    conn.commit()
    conn.close()

def main():
    """ Main Functional"""

    table_create()

    report_date = input("Informe a data desejada (Exemplo: 20171026): ")
    #report_date = "20171026" #date.today() - timedelta(1)
    tree = fromstring(get_stone_report(report_date))

    gross_amount = get_gross_amount(tree)
    net_amount = get_net_amount(tree)
    tax = gross_amount - net_amount
    prevision = builtins.dict(get_prevision(tree))

    print("Valor bruto das transações: R$ {:.02f}".format(gross_amount))
    print("Valor líquído das transações: R$ {:.02f}".format(net_amount))
    print("Total descontado: R$ {:.02f}".format(tax))
    print("Os valores líquidos serão repassados com a seguinte previsão:")
    for x, k in prevision.items():
        print("Data: {} Valor: R$ {:.02f}".format(x, sum(k)))
        insert_data(report_date, x, sum(k))


if __name__ == '__main__':
    main()