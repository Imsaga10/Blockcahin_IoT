# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 09:14:39 2022

@author: Sagar
"""

import ipfshttpclient
client = ipfshttpclient.connect('/dns/ipfs.infura.io/tcp/5001/httpsI')

encfile_hash = client.add("app.py")
print(encfile_hash['Hash'],encfile_hash['Name'])  
