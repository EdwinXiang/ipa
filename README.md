#使用Python自动化打包脚本

* [概要](#gaiyao)
* [Python学习资料](#learn)
* [xocde命令行打包](#xcodebuild)
* [自动化打包使用方法](#auto)
* [python编译器](#python)


<span id = "gaiyao"></span> 
##概要
   在工作中经常遇到这样的问题，每天都在更新bug，测试也一直问我们要新的安装包，奈何每次打包流程都很麻烦，都要半个小时左右，很耗时耗力，那么有什么快捷可以走呢？答案是肯定的，使用`xcodebuild`命令行加`Python`脚本，一键搞定打包，快捷，方便，一次配置终身受益，你值得拥有，好了，废话不多说，直接开始撸吧！

<span id = "learn"></span>
## Python学习资料   
工欲善其事必先利其器，最好的学习资料莫过于官网的文档了，但是对于菜鸟来说，一开始看文档肯定是很吃力的，还有就是英语水平不好的，骚年，先去学习英语吧！这里贴出学习地址：
* [廖雪峰python学习教程](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

* [菜鸟教程python](http://www.runoob.com/python/python-tutorial.html)
* [Python官方文档](https://docs.python.org/2.7/library/index.html)

<span id = "xcodebuild"></span>
##xcode命令行打包

苹果除了工程打包外，还支持使用命令行打包，这也许就是苹果的强大之处。那么要想使用`xcodebuild`顺利打包，你还得安装苹果的`command tool` 命令行工具，安装这个的方法就请自行百度了，因为在这里不是重点。在这里主要想说的就是如何使用命令行打包。
 * [苹果xcodebuild 文档](https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/man.1.html#//apple_ref/doc/man/1/man)
 
xcodebuild builds one or more targets contained in an Xcode project, or builds a scheme contained in an Xcode workspace or Xcode project.  这句话的意思是xcodebuild联编构建包含在Xcode项目的一个或多个目标，或者构建包含在一个方案Xcode的工作区或Xcode项目
```



XCODEBUILD(1)             BSD General Commands Manual            XCODEBUILD(1)

NAME
     xcodebuild -- build Xcode projects and workspaces

SYNOPSIS
     xcodebuild [-project projectname] [-target targetname ...] [-configuration configurationname]
                [-sdk [sdkfullpath | sdkname]] [buildaction ...] [setting=value ...]
                [-userdefault=value ...]
     xcodebuild [-project projectname] -scheme schemename [-destination destinationspecifier]
                [-destination-timeout value] [-configuration configurationname]
                [-sdk [sdkfullpath | sdkname]] [buildaction ...] [setting=value ...]
                [-userdefault=value ...]
     xcodebuild -workspace workspacename -scheme schemename [-destination destinationspecifier]
                [-destination-timeout value] [-configuration configurationname]
                [-sdk [sdkfullpath | sdkname]] [buildaction ...] [setting=value ...]
                [-userdefault=value ...]
     xcodebuild -version [-sdk [sdkfullpath | sdkname]] [infoitem]
     xcodebuild -showsdks
     xcodebuild -list [-project projectname | -workspace workspacename]
     xcodebuild -exportArchive -exportFormat format -archivePath xcarchivepath -exportPath destinationpath
                [-exportProvisioningProfile profilename] [-exportSigningIdentity identityname]
                [-exportInstallerIdentity identityname]

```

当我们是xcode创建的默认工程的时候，我们就使用 `xcodebuild [-project projectname] [-target targetname ...] [-configuration configurationname]`命令，当我们使用cocoapods等创建的workspace项目的时候就使用`xcodebuild -workspace workspacename -scheme schemename [-destination destinationspecifier]`，另外 需要注意的是，project工程后缀.xcodeproj 是可以省略的，但是workspace的工程`MyWorkspace.xcworkspace`后缀名是不能省略的，我们可以在后面看到苹果官方给出了一个案例：
```
EXAMPLES
     xcodebuild clean install

     Cleans the build directory; then builds and installs the first target in the Xcode project in the directory from which xcodebuild was started.

     xcodebuild -target MyTarget OBJROOT=/Build/MyProj/Obj.root SYMROOT=/Build/MyProj/Sym.root

      Builds the target MyTarget in the Xcode project in the directory from which xcodebuild was started, putting intermediate files in the directory /Build/MyProj/Obj.root and the products of the build in the directory /Build/MyProj/Sym.root.xcodebuild -sdk macosx10.6
       Builds the Xcode project in the directory from which xcodebuild was started against the Mac OS
              X 10.6 SDK.  The canonical names of all available SDKs can be viewed using the -showsdks
              option.

     xcodebuild -workspace MyWorkspace.xcworkspace -scheme MyScheme

              Builds the scheme MyScheme in the Xcode workspace MyWorkspace.xcworkspace.

     xcodebuild -workspace MyWorkspace.xcworkspace -scheme MyScheme archive

              Archives the scheme MyScheme in the Xcode workspace MyWorkspace.xcworkspace.

     xcodebuild -workspace MyWorkspace.xcworkspace -scheme MyScheme -destination 'platform=OS X,arch=x86_64'
              test

              Tests the scheme MyScheme in the Xcode workspace MyWorkspace.xcworkspace using the destination
              described as My Mac 64-bit in Xcode.

     xcodebuild -workspace MyWorkspace.xcworkspace -scheme MyScheme -destination 'platform=iOS
              Simulator,name=iPhone' -destination 'platform=iOS,name=My iPad' test

              Tests the scheme MyScheme in the Xcode workspace MyWorkspace.xcworkspace using both the iOS
              Simulator configured as an iPhone and the the iOS device named My iPad.  (Note that the shell
              requires arguments to be quoted or otherwise escaped if they contain spaces.)

     xcodebuild -workspace MyWorkspace.xcworkspace -scheme MyScheme -destination generic/platform=iOS build

              Builds the scheme MyScheme in the Xcode workspace MyWorkspace.xcworkspace using the generic
              iOS Device destination.

     xcodebuild -exportArchive -exportFormat IPA -archivePath MyMobileApp.xcarchive -exportPath
              MyMobileApp.ipa -exportProvisioningProfile 'MyMobileApp Distribution Profile'

              Exports the archive MyMobileApp.xcarchive as an IPA file to the path MyMobileApp.ipa using the
              provisioning profile MyMobileApp Distribution Profile.

     xcodebuild -exportArchive -exportFormat APP -archivePath MyMacApp.xcarchive -exportPath MyMacApp.pkg
              -exportSigningIdentity 'Developer ID Application: My Team'

              Exports the archive MyMacApp.xcarchive as a PKG file to the path MyMacApp.pkg using the appli-cation application
              cation signing identity Developer ID Application: My Team.  The installer signing identity
              Developer ID Installer: My Team is implicitly used to sign the exported package.

```


我这里只是把官方的如何使用xcodebuild给大家贴出来，如何使用以及一些参数的含义，官方文档已经解释的够清楚了，我就不多说了。当你把`python` 和 `xcodebuild `都弄明白之后，打包已经变得不再困难！！下面我们就用脚本来进行打包吧！

<span id = "auto"></span>
##自动化打包使用方法
#### 自动化打包步骤
*  使用python编译环境
*  运行脚本
*  脚本配置文件及参数说明
*  重要代码解释



*****


- - -
##### 使用Python编译环境
使用Python编译环境：在Mac上面有三种方式，第一就是使用终端运行脚本，Mac上面自带Python，打开终端，输入`Python`就可以得到你当前Python的版本号
```
EdwindeAir:~ WeiXiang$ python
Python 2.7.10 (default, Oct 23 2015, 19:19:21) 
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 

```
输入`control+D`退出当前运行环境；运行脚本使用命令：`python xxx.py`回车就OK！

*****

第二个是使用**sublime text** 这个功能很强大，并且可以跨平台开发，支持多种语言。它里面也有很强大的插件，强烈推荐使用这个进行编写代码。sublime text 配置python的运行环境请大家自行百度安装了，怎么使用sublime text 安装插件昨天黄老师已经给大家说了，我就不再重复了；

*****

第三个就是**Pycharm**，不过这个需要购买才能使用，好在网上有很多破解教程，搜搜吧，一学就会了！
[pycharm官方下载地址](http://www.jetbrains.com/pycharm/)

界面看起来也是清爽，代码提示很友好，值得推荐：


![6A88D2BA-DEBD-495D-9D2A-2ABFBB949016.png](http://a3.qpic.cn/psb?/V14A8Rvc2ToEea/ybNRN5xV0z55rz.RzXMkoi6Bsf33lCpGdPFihqZR*ZE!/b/dKcAAAAAAAAA&bo=YgSAAgAAAAAFB8A!&rf=viewer_4)
使用起来也是很简单，下面运行脚本我将用Pycharm来给大家演示


*****

最后一个当然就是xcode了，xcode本来就是很强大的编辑器，但是xcode没有代码提示，这对于新手用起来就很尴尬。反正我用的比较少。
好了  接下来进入最重要的环节，运行脚本

##### 运行脚本

* [x]将脚本放在工程的同级目录下，然后将脚本添加到Pycharm,直接将脚本拖进去就好了。

![path.png](http://a1.qpic.cn/psb?/V14A8Rvc2ToEea/2n*cCRTFC9adFDDDSB7aiMJ1DfMC6tVWxSOPHx9mef0!/b/dKsAAAAAAAAA&bo=.wKuAQAAAAAFAHU!&rf=viewer_4)
* [x]将代码拖到Pycharm下面，然后点击工具栏的run 选择run... 脚本就跑起来了

![running.png](http://a3.qpic.cn/psb?/V14A8Rvc2ToEea/AH0lo*W8JRIiIze6vjq1W9vfINkJZyvn9aySb0t9*e4!/b/dPgAAAAAAAAA&bo=eQSAAgAAAAAFANw!&rf=viewer_4)
* [x]脚本运行成功会有打包成功和上传到第三方内测平台的提示信息，可根据此信息来判断是否运行成功。有些时候上传到第三方平台可能失败，如果网络不好的话。需要手动将IPA添加到三方内测平台。上传成功后会向测试人员发送更新包的邮件。
![success.png](http://a1.qpic.cn/psb?/V14A8Rvc2ToEea/cMd8Di*h9fxRAE1VsE6OHAB7OxpiqqjCKq5e7st1WfY!/b/dK4AAAAAAAAA&bo=TQSAAgAAAAAFAOg!&rf=viewer_4)


##### 脚本配置文件及参数说明
 *****
- [ ] 工程的配置参数如下
- projectName 工程名
- methodType 工程类型  如果是xcode默认工程 那么就是==project==  如果是cocoapods工程那么就是==workspace==
- emailFromUser 邮件发送方
- emailToUser  邮件接收方
- emailPassword  第三方登录授权码
- smtpserver  SMTP地址
- USER_KEY 蒲公英三方内测平台的用户key
- API_KEY 蒲公英内测平台的API KEY

![config.png](http://a3.qpic.cn/psb?/V14A8Rvc2ToEea/bPrj7R0XL0Qx2Z8EXPsx4qO0JB36XKH0a6gyhprLcFU!/b/dLAAAAAAAAAA&bo=FQP9AAAAAAAFAMg!&rf=viewer_4)

-----

关于配置工程文件，你可以这么使用：
在终端输入 `python ipa.py -c` 然后就会提示你输入相关参数了  配置好之后 输入`python ipa.py`就可以去抽个烟等待奇迹的出现！！！

* * *

##### 重要代码解释

-----

`def` 是Python定义函数的方法，有参数就在括号内传入参数，没有就不写，`global` 全局参数，这么写是为了拿到外面配置的`projectName` 工程名,`os,system`要执行的系统命令，这个是Python的内联模块，直接引入就可以使用，`xcodebuld -shceme %s clean` 要清楚的工程名，这一步确保工程正确无误。
```
#清理工程 
def cleanWorkspaceProject():
    global projectName
    os.system('xcodebuild -scheme %s clean'%projectName)
    return
```

-----
最重要的一步，生成app的安装包，需要说明一点的就是 如果工程是`project`的话就需要使用`-target`，如果工程的cocoapods创建的话 就需要使用`-scheme`参数，这两个在默认情况下参数名是一样的。`-configuration`是你打包的类型，包括`debug`和`release`两种，根据你的需求来选择吧。`CODE_SIGN_IDENTITY`这个是证书名。
```
#生成 Project APP包
def creatWorkspaceApp():
    global projectName
    os.system('xcodebuild -workspace %s.xcworkspace -scheme %s -sdk iphoneos -configuration Release build CODE_SIGN_IDENTITY="%s"'%(projectName,projectName,CODE_SIGN_IDENTITY))
    return
```

-----

前面两步成功过后，到这一步就不会成问题了，这一步就是讲app打包成手机可以安装的ipa。`userHome = os.path.expanduser('~')`这句代码是Python的获取当前用户目录的指令。`-v`指向app安装包的路径，拿到这个路径才能给去编译打包成ipa，这里我统一修改成指定的目录。你需要在你的xcode下去修改这个路径，不然会报错的。修改路径：xcode->perferrence->locations->Advanced 修改成你想要的路径就好了。`IPAPath = projectPath + '/' + tempFinder + '/' + projectName + '.ipa'`这一步代码是拿到ipa 的路径拼接。
```
def cerateWorkspaceIpa():
    global projectPath
    global projectName
    global IPAPath
    print "temfinder==========================================================",tempFinder
    userHome = os.path.expanduser('~')
    os.system('xcrun -sdk iphoneos PackageApplication -v %s/Library/Developer/Xcode/DerivedData/Build/Products/Release-iphoneos/%s.app -o %s/%s/%s.ipa'%(userHome,projectName,projectPath,tempFinder,projectName))
    IPAPath = projectPath + '/' + tempFinder + '/' + projectName + '.ipa'
    return

```

*****




<span id = "python"></span> 
##Python编译器
 * Pycharm
 * sublime text
 * xcode
 * terminal


*****

要保证次脚本正常运行  你需要安装python的两个模块`JSON`和`requests` 其他模块都是内置的，关于安装模块的方法请自行百度了，Google很强大的！

																	August 19, 2016 5:14 PM