import mysql.connector
from mysql.connector import Error
import pika

import modules.config as cfg


def query_toBase(query):
    conn = mysql.connector.connect(host=cfg.database['host'],
                                   database=cfg.database['db'],
                                   user=cfg.database['user'],
                                   password=cfg.database['password'])

    cursor = conn.cursor(buffered=True)
    cursor.execute(query)
    res = 'none'
    try:
        row = cursor.fetchall()
        if row:
            res = row
        else:
            res = False
    except Error as e:
        pass

    conn.commit()
    cursor.close()
    conn.close()
    return res


def toRabbit(query):
    crd = pika.PlainCredentials(cfg.rMQ['user'], cfg.rMQ['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=crd,
                                         host=cfg.rMQ['host']))
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='vmstats',
                          body=query)
    connection.close()
    return True
