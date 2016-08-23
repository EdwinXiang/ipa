#!usr/bin/python
# coding=utf-8

import optparse
import os
import sys
import getpass
import json
import time
from optparse import OptionParser
import subprocess
import requests
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

#配置文件路径
commendPath = "/Users/" + getpass.getuser() + "/"
commendFinderName = ".ipa_build_py"
commendFullPath = commendPath + commendFinderName
configFileName = "ipaBuildPyConfigFile.json"
commendFilePath = commendFullPath + "/" + configFileName

#工程路径
projectPath = ''
#工程名
projectName = None
#时间文件夹
tempFinder = None
#时间格式
timeFile = None
#生成的ipa包路径
IPAPath = None
# 工程类型
methodType = None
#下载地址
downUrl = None
# 邮件发送者
emailFromUser = None
# 邮件接收者
emailToUser = None
# 服务器地址
smtpserver = None

contentText = None

# 授权密码
emailPassword = None
#证书  目前只支持企业账号打包
CODE_SIGN_IDENTITY = "iPhone Distribution: xxxxxx, Ltd."

# 蒲公英内侧平台配置信息
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
#userkey 和apikey 在个人信息里面找到修改成你的信息
USER_KEY = None
API_KEY = None

#进入当前工程路径
def cdDir():
    global projectPath
    global projectName
    global methodType
    if not projectName:
        projectName = raw_input('please input projectName:')
    if not methodType:
        methodType = raw_input('please input methodType:')
    curdir = os.getcwd()
    projectPath = curdir + os.sep + projectName
    while not os.path.exists(projectPath):
        projectPath = raw_input('input %s is not exists,please input again:'%projectName)
    try:
        print 'cd %s...' %projectPath
        os.chdir(projectPath)
    except Exception as e:
        print 'catch exception:%s' % e
        exit(1)


# 显示已有的参数
def showParameter():
    print "projectName                 :%s" % projectName
    print "methodType                    :%s" % methodType
    print "emailFromUser            :%s" % emailFromUser
    print "emailToUser                   :%s" % emailToUser
    print "emailPassword              :%s" % emailPassword
    print "smtpserver                :%s" % smtpserver
    print "USER_KEY              :%s" % USER_KEY
    print "API_KEY                  :%s" % API_KEY

# 设置参数
def setParameter():
    global projectName
    global methodType
    global emailFromUser
    global emailToUser
    global emailPassword
    global smtpserver
    global USER_KEY
    global API_KEY
    projectName = raw_input("input projectName:")
    methodType = raw_input("input methodType:")
    emailFromUser = raw_input("input emailFromUser:")
    emailToUser = raw_input("input emailToUser:")
    emailPassword = raw_input("input emailPassword:")
    smtpserver = raw_input("input smtpserver:")
    USER_KEY = raw_input("input USER_KEY:")
    API_KEY = raw_input("input API_KEY:")
    # 保存到本地
    writeJsonFile()


# 判断字符串是否为空
def isNone(para):
    if para == None or len(para) == 0:
        return True
    else:
        return False


# 是否需要设置参数
def isNeedSetParameter():
    if isNone(projectName) or isNone(methodType) or isNone(smtpserver) or isNone(USER_KEY) or isNone(
            emailFromUser) or isNone(emailToUser) or isNone(emailPassword) or isNone(API_KEY):
        return True
    else:
        return False


# 参数设置
def setOptparse():
    p = optparse.OptionParser()
    # 参数配置指令
    p.add_option("--config", "-c", action="store_true", default=None, help="config User's data")
    options, arguments = p.parse_args()
    # 配置信息
    if options.config == True and len(arguments) == 0:
        configMethod()

#配置信息
def configMethod():
    os.system("clear")
    readJsonFile()
    print "您的参数如下:"
    print "************************************"
    showParameter()
    print "************************************"
    setParameter()
    sys.exit()


#设置配置文件路径
def createFinder():
    #没有文件夹，创建文件夹
    if not os.path.exists(commendPath + commendFinderName):
        os.system("cd %s;mkdir %s"%(commendPath,commendFinderName))
    #没有文件，创建文件
    if not os.path.isfile(commendFilePath):
        os.system("cd %s;touch %s"%(commendFullPath,configFileName))
        initJsonFile()
    return


# 初始化json配置文件
def initJsonFile():
    fout = open(commendFilePath, 'w')
    js = {}
    js["projectName"] = None
    js["methodType"] = None
    js["smtpserver"] = None
    js["emailFromUser"] = None
    js["emailToUser"] = None
    js["emailPassword"] = None
    js["USER_KEY"] = None
    js["API_KEY"] = None
    outStr = json.dumps(js, ensure_ascii=False)
    fout.write(outStr.strip().encode('utf-8') + '\n')
    fout.close()


# 读取json文件
def readJsonFile():
    fin = open(commendFilePath, 'r')
    for eachLine in fin:
        line = eachLine.strip().decode('utf-8')
        line = line.strip(',')
        js = None
        try:
            js = json.loads(line)
            global projectName
            global methodType
            global USER_KEY
            global API_KEY
            global smtpserver
            global emailFromUser
            global emailToUser
            global emailPassword
            projectName = js["projectName"]
            methodType = js["methodType"]
            USER_KEY = js["USER_KEY"]
            API_KEY = js["API_KEY"]
            emailFromUser = js["emailFromUser"]
            emailToUser = js["emailToUser"]
            emailPassword = js["emailPassword"]
            smtpserver = js["smtpserver"]
        except Exception, e:
            print Exception
            print e
            continue
    fin.close()


# 写json文件
def writeJsonFile():
    showParameter()
    try:
        fout = open(commendFilePath, 'w')
        js = {}
        js["projectName"] = projectName
        js["methodType"] = methodType
        js["smtpserver"] = smtpserver
        js["emailFromUser"] = emailFromUser
        js["emailToUser"] = emailToUser
        js["emailPassword"] = emailPassword
        js["API_KEY"] = API_KEY
        js["USER_KEY"] = USER_KEY
        outStr = json.dumps(js, ensure_ascii=False)
        fout.write(outStr.strip().encode('utf-8') + '\n')
        fout.close()
    except Exception, e:
        print Exception
        print e


def reatIPAFinder():
    global timeFile
    global tempFinder
    global projectName
#    获取当前本地时间并格式化 年月日
    timeFile = time.strftime("%Y-%m-%d", time.localtime())
    tempFinder = projectName + '-' + timeFile
    if not os.path.exists(tempFinder):
        os.mkdir(tempFinder)
    return
#===========================workspace工程自动打包=====================================#
#清理工程
def cleanWorkspaceProject():
    global projectName
    os.system('xcodebuild -scheme %s clean'%projectName)
    return

#生成 Project APP包
def creatWorkspaceApp():
    global projectName
    os.system('xcodebuild -workspace %s.xcworkspace -scheme %s -sdk iphoneos -configuration Release build CODE_SIGN_IDENTITY="%s"'%(projectName,projectName,CODE_SIGN_IDENTITY))
    return

def cerateWorkspaceIpa():
    global projectPath
    global projectName
    global IPAPath
    print "temfinder==========================================================",tempFinder
    userHome = os.path.expanduser('~')
    os.system('xcrun -sdk iphoneos PackageApplication -v %s/Library/Developer/Xcode/DerivedData/Build/Products/Release-iphoneos/%s.app -o %s/%s/%s.ipa'%(userHome,projectName,projectPath,tempFinder,projectName))
    IPAPath = projectPath + '/' + tempFinder + '/' + projectName + '.ipa'
    return

#===========================project工程自动打包=======================================#
#清理工程
def cleanProject():
    global projectName
    os.system('xcodebuild -target %s clean'%projectName)
    return

#生成APP包
def creatProkectApp():
    global projectName
    os.system('xcodebuild -target %s -configuration Release build CODE_SIGN_IDENTITY="%s"'%(projectName,CODE_SIGN_IDENTITY))
    return

def cerateProjectIpa():
    global projectPath
    global projectName
    global IPAPath
    print "=========================================================="
    os.system('xcrun -sdk iphoneos PackageApplication -v %s/build/Release-iphoneos/%s.app -o %s/%s/%s.ipa'%(projectPath,projectName,projectPath,tempFinder,projectName))
    IPAPath = projectPath + '/' + tempFinder + '/' + projectName + '.ipa'
    return

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendEmailToTester():
    global emailFromUser
    global emailToUser
    global emailPassword
    global smtpserver
    global downUrl
    global contentText
#    msg = MIMEText('张浩你好，新的测试包已上传，请测试', 'text', 'utf-8')
    textCotnent = '<html><body><h1>Hello,zhangHao</h1><p>send by <a href="' + downUrl + '">tianyanAR</a>...</p></body></html>'
        
    print "contentText : ",contentText
    msg = MIMEText(textCotnent, 'html', 'utf-8')
#    msg['From'] = _format_addr('IOS开发者 <%s>' % emailFromUser)
#    msg['To'] = _format_addr('管理员 <%s>' % emailToUser)
    msg['From'] = emailFromUser
    msg['To'] = emailToUser
    msg['Subject'] = Header('测试包更新了', 'utf-8').encode()
    try:
        server = smtplib.SMTP(smtpserver, 25)
        server.set_debuglevel(1)
        server.login(emailFromUser, emailPassword)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print '发送成功'
    except Exception, e:
        print str(e)

def parserUploadResult(jsonResult):
    global DOWNLOAD_BASE_URL
    global downUrl
    resultCode = jsonResult['code']
    if resultCode == 0:
        downUrl = DOWNLOAD_BASE_URL +"/"+jsonResult['data']['appShortcutUrl']
        print "Upload Success"
        print "DownUrl is:" + downUrl
    else:
        print "Upload Fail!"
        print "Reason:"+jsonResult['message']

def uploadIpaToPgyer():
    global IPAPath
    global USER_KEY
    global API_KEY
    global PGYER_UPLOAD_URL
    print "ipaPath:",IPAPath
    files = {'file': open(IPAPath, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'2','isPublishToPublic':'2', 'password':'123'}
    print "uploading...."
    r = requests.post(PGYER_UPLOAD_URL, data = payload ,files=files,headers=headers)
    if r.status_code == requests.codes.ok:
        result = r.json()
        parserUploadResult(result)
    else:
        print 'HTTPError,Code:'+r.status_code
def judgeUploadToPgyerSuccess():
    global downUrl
    if len(downUrl) > 20:
        print "上传成功"
        sendEmailToTester()
    else:
        print "上传失败"
    return

def choosePackageApplicationMethod():
    # 设置配置文件路径
    createFinder()
    # 参数设置
    setOptparse()
    # 读取json文件
    readJsonFile()
    # 是否需要设置参数
    if isNeedSetParameter():
        print "您需要设置参数,您的参数如下(使用 --config 或者 -c):"
        showParameter()
        sys.exit()
    cdDir()
    reatIPAFinder()
    if methodType == "workspace":
        cleanWorkspaceProject()
        creatWorkspaceApp()
        cerateWorkspaceIpa()
    else:
        cleanProject()
        creatProkectApp()
        cerateProjectIpa()
    uploadIpaToPgyer()
    judgeUploadToPgyerSuccess()

if __name__ == '__main__':
    choosePackageApplicationMethod()
