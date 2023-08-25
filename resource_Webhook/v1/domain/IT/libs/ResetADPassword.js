var execFile = require('child_process').execFile;
const { exec } = require("child_process");
var generator = require('generate-password');


class ResetAD {
    
    
    constructor(config) {
    
        this.config = config;
        this.response1=0;
        this.res=0
        this.resetadpassword = this.resetadpassword.bind(this);
    }
 
   resetadpassword(accountname,password){
        
        console.log("------------Microclinic-------------",accountname)
     
        var user = "abbas.abbas"
        var domainName = '192.168.10.10'
        var ADadminuser = 'ta.operator'
        var ADdminpassword  = 'NSoTQyrmf+zPlK0te5txWMFDjz7cnU2d3N3V7uXBk4U='
      
// send temporary password via e-mail 
        var emailID = 'service.desk@tigeranalytics.com'
        var emailpassword='dGHPHMqU1IixtqsEFzSyzo+EIBQ3YrCLoBJIaANPl6lDUF37yK3jhynUvQxwZCLN'
//// end 
        
        var executablePath = "C:\\temp\\resetPassword\\newExe\\ADPassChangeEmail.exe";

        var randomPassword=password;
        execFile(executablePath, [`${user}`,`${domainName}`,`${ADadminuser}`,`${ADdminpassword}`,`${emailID}`,`${emailpassword}`,`${randomPassword}`], function(err, data) {
        if(err) {
            console.log('error123333',err)
            this.res=0  
        } 
        else {
            console.log("exe-output",data.toString());   
            this.res=1
        }
        console.log("this.response1",this.response1)  
        return this.response1

    }); 
    
    console.log(this.response1,'final-msg')
    
}
}
module.exports = ResetAD;