#!/usr/bin/python

import json
from elasticsearch import Elasticsearch
import sys
import time
from datetime import datetime


class StatusBar():
    casser = False

    def recherche(self, id):
         es = Elasticsearch()
         query = "alert.signature_id:" + str(id)
         matches = es.search(q=query, filter_path=['hits.hits._source.timestamp'], sort='timestamp:desc')
         hits = matches['hits']['hits']
         if not hits:
             return None
         else:
             return hits[0]['_source']['timestamp']

    def netRecherche(self, id):
         es = Elasticsearch()
         query = "alert_signature_id:" + str(id)
         matches = es.search(q=query, filter_path=['hits.hits._source.timestamp'], sort='timestamp:desc')
         hits = matches['hits']['hits']
         if not hits:
             return None
         else:
             return hits[0]['_source']['timestamp']



    def appStatus(self):
        format='%Y-%m-%dT%H:%M:%S.%f'
        timePing = self.recherche('2013504').split('+')[0]
        timePong = self.recherche('2013504').split('+')[0]
        timeAdmin = self.recherche('2013504').split('+')[0]
        tPing = datetime.strptime(timePing,format)
        tPong = datetime.strptime(timePong,format)
        tAdmin = datetime.strptime(timeAdmin,format)
        if tAdmin<tPing and tAdmin<tPong:
            self.casser = True
            return "Admin"
        elif tPing<tPong:
            return "Ping"
        else:
            return "Pong"

    def netStatus(self):
        format='%Y-%m-%dT%H:%M:%S.%f'
        timePing = self.netRecherche('2013504').split('+')[0]
        timePong = self.netRecherche('2013504').split('+')[0]
        timeAdmin = self.netRecherche('2013504').split('+')[0]
        tPing = datetime.strptime(timePing,format)
        tPong = datetime.strptime(timePong,format)
        tAdmin = datetime.strptime(timeAdmin,format)
        if tAdmin<tPing and tAdmin<tPong:
            self.casser = True
            return "Admin"
        elif tPing<tPong:
            return "Ping"
        else:
            return "Pong"
        return timePing

    def isAttack(self):
        if self.casser:
            self.casser = False
            return "True"
        else:
            return "False"

    def refresh(self):
        sys.stdout.write('\r')
        sys.stdout.write('App-status: ')
        sys.stdout.write(str(self.appStatus()))
        sys.stdout.write(' | Net-status: ')
        sys.stdout.write(str(self.netStatus()))
        sys.stdout.write(' | Attaque: ')
        sys.stdout.write(self.isAttack())
        sys.stdout.flush()

if __name__ == "__main__":
    Bar = StatusBar()
    a = 0

    while a<20:
        Bar.refresh()
        time.sleep(0.25)
        a=a+1
