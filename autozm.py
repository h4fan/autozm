#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, requests, sqlite3, math

db_str = 'ipport.db'

APIKEY_ZE = "replace with your api key"

def log2db(cidrstr, ip, port, service, hostname, app, title ):

    conn = sqlite3.connect(db_str)
    c = conn.cursor()

    #print(logtimestamp,src_ip,iplocation,datatype,hostname,fulldata,isshow)
    c.execute("insert into records values(?,?,?,?,?,?,?)",(cidrstr, str(ip), port, str(service), str(hostname), str(app), str(title)))
    conn.commit()
    conn.close()



def getrecords():
    conn = sqlite3.connect(db_str)
    c = conn.cursor()
    #print(logtimestamp,src_ip,iplocation,datatype,hostname,fulldata,isshow)

    c.execute("select distinct cidrstr from records")
    values = c.fetchall()
    result = []
    for row in values:
        result.append(row[0])

    conn.commit()
    conn.close()
    return result


def getelement(thedict, element):
    if(element in thedict.keys()):
        return thedict[element]
    else:
        return ""


def dealresult(res_str, cidr):
    matches = res_str["matches"]
    for rec in matches:
        portinfo = rec["portinfo"]
        print(cidr, getelement(rec,"ip"),getelement(portinfo,"port"),getelement(portinfo,"service"),getelement(portinfo,"hostname"),getelement(portinfo,"app"),getelement(portinfo,"title"))
        log2db(cidr, getelement(rec,"ip"),getelement(portinfo,"port"),getelement(portinfo,"service"),getelement(portinfo,"hostname"),getelement(portinfo,"app"),getelement(portinfo,"title"))

    return (res_str["available"], len(matches))



def getcidrresult(cidr, morepageflag = False):
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",\
    "API-KEY":APIKEY_ZE}
    r = requests.get(url = 'https://api.zoomeye.org/host/search?query=%s&page=1' % cidr, headers = headers)
    resp = r.json()
    tmpresult = dealresult(resp, cidr)
    available = tmpresult[0]
    matchlen = tmpresult[1]
    print("[results]",available)
    if morepageflag:
        for i in range(2,math.ceil(available/20)+1):
            r = requests.get(url = 'https://api.zoomeye.org/host/search?query=%s&page=%d' % (cidr, i), headers = headers)
            tmpresult = dealresult(r.json(), cidr)
            if(tmpresult[1] == 0):
                print("getting no result, break")
                break


with open("cidr.txt","r") as fin:
    lines = fin.readlines()
    loggedrec = getrecords()
    for line in lines:
        line = line.strip()
        if (line+"/24" in loggedrec):
            print("skipped:",line)
            continue
        getcidrresult(line+"/24", True)
