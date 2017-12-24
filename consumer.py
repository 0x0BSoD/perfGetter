#!/usr/bin/env python3
import pika

from modules.mysql_wraper import query_toBase
import modules.config as cfg

crd = pika.PlainCredentials(cfg.rMQ['user'], cfg.rMQ['password'])
connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=crd,
                                     host=cfg.rMQ['host']))
channel = connection.channel()


def callback(ch, method, properties, body):
    tmp = body.decode()
    print("[x] Get: {0}".format(tmp))
    print("=======================================================")
    query_toBase(tmp)


channel.basic_consume(callback, queue='vmstats', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
