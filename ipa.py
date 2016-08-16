#!usr/bin/python
# coding=utf-8

import os
import sys
import time
from optparse import OptionParser
import subprocess
import requests

projectPath = ''
projectName = ''
tempFinder = None
timeFile = None
IPAPath = None
methodType = None

#证书  目前只支持企业账号打包
CODE_SIGN_IDENTITY = "iPhone Distribution: Weily Interactive Technology Co., Ltd."

# 蒲公英内侧平台配置信息
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
#userkey 和apikey 在个人信息里面找到修改成你的信息
USER_KEY = "0cdecee7a8baa0d6ea95e25ef12b8337"
API_KEY = "32d956c50ee40525e665d73adf08fd59"

#进入当前工程路径
def cdDir():
    global projectPath
    global projectName
    global methodType
    argv = sys.argv
    count = len(argv)
    if count < 3:
        projectName = raw_input('please input projectName:')
        methodType = raw_input('please input methodType:')
    else:
        projectName = argv[1]
        methodType = argv[2]
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

def parserUploadResult(jsonResult):
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

def choosePackageApplicationMethod():
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


if __name__ == '__main__':
    choosePackageApplicationMethod()
