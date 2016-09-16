import os
import sys
import requests
import base64
import plistlib


def authenticate_user(appleid, password):
    
    strAuth = "{mail}:{passid}".format(mail=appleid,passid=password)
    b64Auth = base64.b64encode(strAuth)
    #print b64Auth
    
    try:
        response = requests.get(
            
            url="https://setup.icloud.com/setup/authenticate/{mail}".format(mail=appleid),
            
            headers={
                "User-Agent": "iCloud.exe (unknown version) CFNetwork/520.2.6",
                "Host": "setup.icloud.com",
                "X-Mme-Client-Info": "<PC> <Windows; 6.1.7601/SP1.0; W> <com.apple.AOSKit/88>",
                "Accept-Language": "en-US",
                "Authorization": "Basic {auth}".format(auth=b64Auth),
                "Accept": "*/*",
                },
        )
        #print('Response HTTP Status Code: {status_code}'.format(
        #    status_code=response.status_code))
        
        #print('Response HTTP Response Body: {content}'.format(
        #    content=response.content))
        
        responsePlist = plistlib.readPlistFromString(response.content)
        
        accountId = responsePlist['appleAccountInfo']['dsPrsID']
        authToken = responsePlist['tokens']['mmeAuthToken']
        
        #print "\n{accId}:{aToken}".format(accId=accountId, aToken=authToken) # like the way elcomsoft did
        
        getAccountInfo(accountId, authToken)
    
    except requests.exceptions.RequestException:
            print('HTTP Request failed')
            return
    
    return

# get account info with account id and auth token

def getAccountInfo(accountId, authToken):
    
    # simple auth what apple used
    
    strAuth = "{accId}:{token}".format(accId=accountId, token=authToken)
    b64Auth = base64.b64encode(strAuth)
    
    try:
        response = requests.post(
        url="https://setup.icloud.com/setup/get_account_settings",
        headers={
            "User-Agent": "iCloud.exe (unknown version) CFNetwork/520.2.6",
            "Host": "setup.icloud.com",
            "X-Mme-Client-Info": "<PC> <Windows; 6.1.7601/SP1.0; W> <com.apple.AOSKit/88>",
            "Authorization": "Basic {auth}".format(auth=b64Auth),
            "Accept-Language": "en-US",
            "Accept": "*/*",
            },
    )
        #print('Response HTTP Status Code: {status_code}'.format(
        #status_code=response.status_code))
        
        #print('Response HTTP Response Body: {content}'.format(
        #content=response.content))
        
        # get response as plist file
        
        responsePlist = plistlib.readPlistFromString(response.content)
        
        # get datas from plist
        
        appleId = responsePlist['appleAccountInfo']['appleId']
        primaryEmail = responsePlist['appleAccountInfo']['primaryEmail']
        fullName = responsePlist['appleAccountInfo']['fullName']
        aliasAppleId = responsePlist['appleAccountInfo']['appleIdAliases']
        isLocked = responsePlist['appleAccountInfo']['locked']
        icloudAppleIdAlias = responsePlist['appleAccountInfo']['iCloudAppleIdAlias']
        
        # print some
        
        print("")
        
        print("Full Name : {fullname}".format(fullname=fullName))
        print("AppleID : {appleid}".format(appleid=appleId))
        print("PrimaryEmail : {pemail}".format(pemail=primaryEmail))
        print("iCloud Apple ID : {icmail}".format(icmail=icloudAppleIdAlias))
        print("AliasAppleIds : {aliasIds}".format(aliasIds=aliasAppleId))
        print("Is Locked : {islocked}".format(islocked=isLocked))
        
        print("")
    
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        return
    
    return

def printAboutMe():
    
    print("\n by TwizzyIndy (github.com/TwizzyIndy) (c) 2016\n")
    return


def main():
    
    # clear the screen
    
    os.system("clear")
    
    if len(sys.argv) < 2:
        print("")
        print("Usage : %s apple_id password" % sys.argv[0])
        print("Usage : %s account_id authToken" % sys.argv[0])
        printAboutMe()
        return
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    
    if not str(arg1).find('@'):
        getAccountInfo(arg1, arg2) # just for tester
        printAboutMe()
        return
    
    authenticate_user(arg1, arg2)
    printAboutMe()
    return
        
        
if __name__ == "__main__":
    main()
