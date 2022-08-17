pragma experimental ABIEncoderV2;

contract BlockchainIOT {

    struct candidateinfo {
        address key;
        string name;
        string dob;
        string mobile;
        string email;
        string password;
    }

    struct Sharefile { 
        address key;
        string filname;
        string uploader;
        string receiver;
        string ipfsfolderhash;
        string encry;
        string privatekey;
    }
    
    struct filedetails { 
        address key;
        string filename;
        string uploader;
        string privatekey;
        string encryptedkey;
        string publickey;
        string ipfsfolderhash;
    }


    mapping (string => address) userAddresses;
    mapping (address => candidateinfo) candidateinfos;
    mapping (address => Sharefile) Sharefiles;
    mapping (address => filedetails) filedetailss;

    candidateinfo[] public allcandidates;
    Sharefile[] public allSharefiles;
    filedetails[] public allfiledetailss;

    event getRecord(string data);
    
    function allRegister(string memory user,  string memory name, string memory dob, string memory mobile, 
    string memory email, string memory password) public {
       
        address pAddr = userAddresses[user];
        candidateinfo memory userinfo1 = candidateinfo(msg.sender,name, dob, mobile, email, password);  
        
        //caseinfos[pAddr].case_id=case_id;//.push(name);
        
        candidateinfos[pAddr].name=name;
        candidateinfos[pAddr].dob=dob;
        candidateinfos[pAddr].mobile=mobile;
        candidateinfos[pAddr].email=email;
        candidateinfos[pAddr].password=password;
        
        allcandidates.push(userinfo1);
       
    }
    
    function allLogin(string memory user,string memory name,string memory password) public returns(candidateinfo[] memory) 
    {
        address pAddr = userAddresses[user];
        candidateinfo[] memory result = new candidateinfo[](allcandidates.length);  // step 2 - create the fixed-length array
        uint256 j;       
        
            for (uint i = 0; i < allcandidates.length; i++)
            {
                if(keccak256(abi.encodePacked(string(allcandidates[i].name)))==keccak256(abi.encodePacked(name)) && keccak256(abi.encodePacked(string(allcandidates[i].password)))==keccak256(abi.encodePacked(password)))
                {

                    emit getRecord(allcandidates[i].name);
                    result[j]=allcandidates[i];
                    j++;
                }
            }
            return result;  
    }

    function getAlluser(string memory user) public returns(candidateinfo[] memory) 
    {
        address pAddr = userAddresses[user];
        candidateinfo[] memory result = new candidateinfo[](allcandidates.length);  // step 2 - create the fixed-length array
        uint256 j;       
        
            for (uint i = 0; i < allcandidates.length; i++)
            {
                emit getRecord(allcandidates[i].name);
                result[j]=allcandidates[i];
                j++;
            }
            return result;  
    }


    function ShareFile(string memory user,  string memory filname, string memory uploader, string memory receiver,string memory ipfsfolderhash,string memory encry,string memory privatekey) public {
       
        address pAddr = userAddresses[user];
        Sharefile memory Sharefile1 = Sharefile(msg.sender,filname, uploader,receiver,ipfsfolderhash,encry,privatekey);  
        
        Sharefiles[pAddr].filname=filname;
        Sharefiles[pAddr].uploader=uploader;
        Sharefiles[pAddr].receiver=receiver;
        Sharefiles[pAddr].ipfsfolderhash=ipfsfolderhash;
        Sharefiles[pAddr].encry=encry;
        Sharefiles[pAddr].privatekey=privatekey;
        
        allSharefiles.push(Sharefile1);
    }
    
    function getShareFile(string memory user,string memory receiver) public returns(Sharefile[] memory) 
    {
        address pAddr = userAddresses[user];
        Sharefile[] memory result = new Sharefile[](allSharefiles.length);  // step 2 - create the fixed-length array
        uint256 j;       
        for (uint i = 0; i < allSharefiles.length; i++)
        {
            if(keccak256(abi.encodePacked(string(allSharefiles[i].receiver)))==keccak256(abi.encodePacked(receiver)))
            {
                emit getRecord(allSharefiles[i].filname);
                result[j]=allSharefiles[i];
                j++;
            }
        }
        return result;  
    }
    
    
    function addFiledetails(string memory user,  string memory filename, string memory uploader, string memory privatekey, string memory encryptedkey, string memory publickey, string memory ipfsfolderhash) public {
       
            address pAddr = userAddresses[user];
            filedetails memory filedetails1 = filedetails(msg.sender,filename, uploader,privatekey,encryptedkey,publickey,ipfsfolderhash);
            
            
            filedetailss[pAddr].filename=filename;
            filedetailss[pAddr].uploader=uploader;
            filedetailss[pAddr].privatekey=privatekey;
            filedetailss[pAddr].encryptedkey=encryptedkey;
            filedetailss[pAddr].publickey=publickey;
            filedetailss[pAddr].ipfsfolderhash=ipfsfolderhash;
            
            allfiledetailss.push(filedetails1);
    }
    
    
    function getfiledetails(string memory user,string memory uploader) public returns(filedetails[] memory) 
    {
        address pAddr = userAddresses[user];
        filedetails[] memory result = new filedetails[](allfiledetailss.length);  // step 2 - create the fixed-length array
        uint256 j;       
        for (uint i = 0; i < allfiledetailss.length; i++)
        {
            if(keccak256(abi.encodePacked(string(allfiledetailss[i].uploader)))==keccak256(abi.encodePacked(uploader)))
            {
                emit getRecord(allfiledetailss[i].filename);
                result[j]=allfiledetailss[i];
                j++;
            }
        }
        return result;  
    }

    
    
}