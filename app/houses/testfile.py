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

if __name__ == '__main__':
	savephoto(2,2)