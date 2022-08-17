# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 19:37:39 2022

@author: INBOTICS
"""
import ipfsApi
api = ipfsApi.Client(host='127.0.0.1', port=5001)

new_file = api.add("2.jpg")
print(new_file['Hash']) 

print(new_file)


import urllib3
# https://ipfs.io/ipfs
url = 'http://127.0.0.1:8080/ipfs/'+new_file['Hash']
connection_pool = urllib3.PoolManager()
resp = connection_pool.request('GET',url )
f = open("newapp.jpg", 'wb')
f.write(resp.data)
f.close()
resp.release_conn()