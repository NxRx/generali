#!/bin/python
import pdb
import sys,os
import argparse
from datetime import datetime,timedelta
from xml.etree import ElementTree as et
import json

class generali(object):
    def __init__(self,choice):
        self.choice = choice
        self.jsonElement = ""
        self.currentDir = os.getcwd()
        self.now = "%s%s%s"%(datetime.now().year,datetime.now().strftime('%m'),datetime.now().strftime('%d'))
        self.callTask()

    def callTask(self):
        if self.choice == 1:
            print("The task here is to update the xml file with given days to current date\n")
            arg1 = input("Enter an integer value for X(day):   ")
            try:
                newX = datetime.strptime(self.now, "%Y%m%d") + timedelta(days= int(arg1))
                newX = ("%s%s%s"%(newX.year,newX.strftime('%m'),newX.strftime('%d')))
            except:
                sys.exit("Day %s provided is not in the proper format"%arg1)           

            arg2 = input("Enter an integer value for Y(day):   ") 
            try:
                newY = datetime.strptime(self.now, "%Y%m%d") + timedelta(days= int(arg2))
                newY = ("%s%s%s"%(newY.year,newY.strftime('%m'),newY.strftime('%d')))
            except:
                sys.exit("Provided day %s is not in proper format"%arg2)

            self.updateDoc(newX,newY)            
        elif self.choice == 2:
            print("The task here is to update the json element\n")
            self.jsonElement = input("Enter a json element to remove:   ")
            jsonFile = '%s/test_payload.json'%self.currentDir
            with open(jsonFile) as temp:
                try:
                    data = json.load(temp)
                    self.removeJsonElement(data)
                except:
                    sys.exit("Cannot open the json file")
        elif self.choice == 3:
            print("The task here is to parse csv file and print non-succesful endpoint log\n")
            self.jmeterLog()
        else:  
            sys.exit("Task choice is wrong")

    def removeJsonElement(self,data):
            for k,v in list(data.items()):
                if k == self.jsonElement:
                    del data[k]
                elif type(v) == dict:
                    self.removeJsonElement(v)
                elif type(v) == list:
                    data[k] = [x for x in v if x != self.jsonElement]    
            with open('test_payload_new.json','w') as temp:
                temp.write(str(data))   

    def jmeterLog(self):
        csvFile = '%s/Jmeter_log1.jtl'%self.currentDir
        with open(csvFile) as temp:
            for i,eachLine in enumerate(temp.readlines()):
                if i == 0:
                    continue
                splitLine = eachLine.split(",")
                tstamp = int(splitLine[0])/1000
                if splitLine[4] != "OK":
                    print("%s :: %s :: %s :: %s ::%s"%(splitLine[2],splitLine[3],splitLine[4],splitLine[8],str(datetime.fromtimestamp(tstamp).strftime("%Y-%m-%d %H:%M:%S"))))
    def updateDoc(self,x,y):
        tree = et.parse('test_payload1.xml')
        tree.find('REQUEST/TP/DEPART').text = x
        tree.find('REQUEST/TP/RETURN').text = y
        tree.write('test_payload_new.xml')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Select task')
    parser.add_argument('-task', type=int, help='Choice of task')

    args = parser.parse_args()
    runCode = generali(args.task)
