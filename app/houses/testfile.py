#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64,os

def savephoto(photolist,id):
    path = "./photo" + str(id)
    mkdir = os.mkdir(path)
    url_list = []
    for i in range(len(photolist)):
    	photopath = path + "/" + str(i)  # ./photo/<house id>/<i>
    	f = open(photopath,'rb')
    	f.write(photolist[i])
    	f.close()
    	url_list.append(photopath)
    return url_list
'''    f1 = open("./photo/house.jpg",'rb')
    f2 = open("./photo/houseb64",'wb+')
    b64c = base64.b64encode(f1.read())
    f2.write(b64c)
    b64d = base64.b64decode(b64c)
#   f3.write(b64d)
    f1.close()
    f2.close()'''



if __name__ == '__main__':
	savephoto(2,2)