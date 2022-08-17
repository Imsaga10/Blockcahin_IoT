from flask import Flask, session
from flask import render_template,request
import os
import random
import json
from web3 import Web3, HTTPProvider

app = Flask(__name__)

UPLOAD_FOLDER = 'static/detecteimages/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'any random string'

from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii        
import urllib3

# import ipfsApi
# api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)

import ipfsApi
api = ipfsApi.Client(host='127.0.0.1', port=5001)

"-----------------------------------------------------------------------------------------------"

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "newbpfile_enc.txt"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:#rb means read in binary
        with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk)%16 != 0:
                    chunk += b' '*(16-(len(chunk)%16))

                outfile.write(encryptor.encrypt(chunk))

def decrypt11(key, filename):
    chunksize = 64*1024
    outputFile = "static/decrypted/newbpfile.txt"
    print('FILEIS',outputFile)
    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor= AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)

def getKey(password):
    hasher = sha256(password.encode('utf-8'))
    return hasher.digest()  

"-----------------------------------------------------------------------------------------------"

# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:9545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Path to the compiled contract JSON file
compiled_contract_path = 'build/contracts/BlockchainIOT.json'

# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x47229e59baBd23c806926E3F5c380Fdda5CCc95A'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
#print(contract_abi)
# Fetch deployed contract reference
contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)


acc1privatekey='36dd68da46dcbca187066a02d3131badff7df543677117068d9426fc49c3acf4'

"-----------------------------------------------------------------------------------------------"


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/main1')
def main1():
    return render_template('index1.html') 

@app.route('/logout')
def logout():
    session.pop('name',None)
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        details = request.form
        
        name = details['name']
        password = details['password']
        
        data = contract.functions.allLogin(web3.eth.accounts[0],name,password).call()
        
        if(len(data) == 0): 
            return "fail"
        else:
            if(data[0][1] == ''):            
                return "fail"
            else: 
                session['user'] = name           
                return "success" 
        
    return render_template('index1.html') 

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == "POST":
        details = request.form
        
        name = details['name']        
        dob = details['dob']
        email = details['email']
        mobile = details['mobile']
        password = details['password']
        print(name,dob,email,mobile,password)
        nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
        print(nonce)
        
        tx_hash1 = contract.functions.allRegister(web3.eth.accounts[0],name,dob,email,mobile,password).buildTransaction({'gas':2000000,'gasPrice':web3.toWei('50','gWei'),'from':web3.eth.accounts[0],'nonce':nonce})
        signed_tx=web3.eth.account.signTransaction(tx_hash1,private_key=acc1privatekey)
        
        tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        print(tx)
        
        return render_template('index.html') 
        
    return render_template('index.html') 

@app.route('/createFile',methods=['POST','GET'])
def createFile():    
    if request.method == "POST":       
        
        bPressure = random.randint(50,100)
        print("Heart rate is : "+str(bPressure))
        file1 = open("newbpfile.txt","w")
        file1.write("Heart rate is : "+str(bPressure))
        file1.close()
        
        key = RSA.generate(2048)

        with open('private.pem', 'wb' ) as f:
            f.write( key.exportKey( 'PEM' ))
            
        filename = "newbpfile.txt"
        password = str(random.randint(1000,9999))
        print(password)
        
        encrypt(getKey(password), filename) 
        
        publicKey = PKCS1_OAEP.new( key )
        secret_message = bytes(password, 'utf-8')
        
        encMessage = publicKey.encrypt( secret_message ) 
        hexilify= binascii.hexlify(encMessage)
        strencry = str(hexilify.decode('UTF-8'))
            
        encfile_hash = api.add("newbpfile_enc.txt")
        print(encfile_hash['Hash'],encfile_hash['Name'])  
        
        privatekey_hash = api.add("private.pem")
        print(privatekey_hash['Hash'],privatekey_hash['Name']) 
        
        username = session.get("user")
        
        data = contract.functions.getfiledetails(web3.eth.accounts[0],username).call()
        
        length = str(len(data)+1)
        print(length) 
        
        # acc1privatekey='8aeff0fd60cb7f155a497909dea0a5969bb54ec0e95a13d70b66e4df8c473e4a'
        nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
        tx_hash1 = contract.functions.addFiledetails(web3.eth.accounts[0],"File_"+length+".txt",username,privatekey_hash['Hash'],strencry,"publickkey",encfile_hash['Hash']).buildTransaction({'gas':2000000,'gasPrice':web3.toWei('50','gWei'),'from':web3.eth.accounts[0],'nonce':nonce})
        signed_tx=web3.eth.account.signTransaction(tx_hash1,private_key=acc1privatekey)
        
        tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
        print("-----------------------")
        print(tx_hash1)
        print("-----------------------")
        print(signed_tx)
        print("-----------------------")
        print(tx)
        print("-----------------------")
        
        os.remove("newbpfile_enc.txt")
        os.remove("newbpfile.txt")
        os.remove("private.pem")
        
        if username == "yash":
            return "success" 
        else:
            return "fail"
    return render_template('uploadFile.html') 

@app.route('/shareFile',methods=['POST','GET'])
def shareFile():
    username = session.get("user")
    data = contract.functions.getfiledetails(web3.eth.accounts[0],username).call()  
    res = [ele for ele in data if ele[1] != '']
  
    return render_template('shareFile.html',rows=res)

@app.route('/shareFile1',methods=['POST','GET'])
def shareFile1():
    if request.method == "POST":        
        details = request.form        
        info = details['alldata']
        
        data=info.split('|')   
        
        alluser = contract.functions.getAlluser(web3.eth.accounts[0]).call()  
        res = [ele for ele in alluser if ele[1] != '']
      
        return render_template('shareFile1.html',data=data,res=res) 
    
@app.route('/Share',methods=['POST','GET'])
def Share():
    if request.method == "POST":        
        details = request.form    
        
        filename = details['filename']    
        uploder = details['uploder']     
        receiver = request.form.get('selecteduser')
        encfile = details['encfile']    
        enctetxt = details['enctetxt']    
        privatekey = details['privatekey']
        
        # acc1privatekey='8aeff0fd60cb7f155a497909dea0a5969bb54ec0e95a13d70b66e4df8c473e4a'
        nonce = web3.eth.getTransactionCount(web3.eth.accounts[0])
        tx_hash1 = contract.functions.ShareFile(web3.eth.accounts[0],filename,uploder,receiver,encfile,enctetxt,privatekey).buildTransaction({'gas':2000000,'gasPrice':web3.toWei('50','gWei'),'from':web3.eth.accounts[0],'nonce':nonce})
        signed_tx=web3.eth.account.signTransaction(tx_hash1,private_key=acc1privatekey)
        
        tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(tx)

        return "success" 
    
@app.route('/receiveFile',methods=['POST','GET'])
def receiveFile():
    username = session.get("user")
    data = contract.functions.getShareFile(web3.eth.accounts[0],username).call()  
    
    res = [ele for ele in data if ele[1] != '']
    return render_template('receivedfiles.html',rows=res)

@app.route('/downloadFile',methods=['POST','GET'])
def downloadFile():
    if request.method == "POST":        
        details = request.form        
        info = details['alldata']
        
        data=info.split('|')
        print(data)

        filename = data[0]
        encfile = data[2]    
        enctetxt = data[3]    
        privatekey = data[4]
        
        url1 = 'http://127.0.0.1:8080/ipfs/'+privatekey
        connection_pool1 = urllib3.PoolManager()
        resp1 = connection_pool1.request('GET',url1 )
        f = open("private.pem", 'wb')
        f.write(resp1.data)
       # print(f)
        f.close()
        resp1.release_conn()
        
        url2 = 'http://127.0.0.1:8080/ipfs/'+encfile
        connection_pool2 = urllib3.PoolManager()
        resp2 = connection_pool2.request('GET',url2 )
        f = open("newbpfile_enc.txt", 'wb')
        f.write(resp2.data)
        #print(f)
        f.close()
        resp2.release_conn()
        
        with open("private.pem",'r' ) as f:
            key = RSA.importKey( f.read() )
        
        str1 = enctetxt 
        convertedtobyte = bytes(str1, 'utf-8')
        public_crypter =  PKCS1_OAEP.new( key )
        decrypted_data = public_crypter.decrypt( binascii.unhexlify(convertedtobyte) )
      #  print(decrypted_data)
        str1 = decrypted_data.decode('UTF-8') 
       # print(str1)
        
        decrypt11(getKey(str(str1)) , "newbpfile_enc.txt")
        outputFilename = "static/decrypted/newbpfile.txt"
        #print(outputFilename)
        # decrypt(getKey(str1),ipfs)        
        return render_template('downloaddisplay.html',filetodisplay=outputFilename,filename=filename)
    
import os
def checking():
    filename='app.py'
    with open(filename) as existing_file:
        existing_file.close()
        os.remove(filename)
        
# checking()

if __name__ == "__main__":
    app.run("0.0.0.0")