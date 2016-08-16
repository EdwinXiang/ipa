# ipa
### 使用python脚本自动打包ipa使用教程
此脚本支持自动打包，支持cocoapods工程和project工程，只需要在运行脚本的时候输入工程名和工程类型：project/workspace 支持将ipa包上传到蒲公英内测平台，以前的打包繁琐事情再也不用担心了，这些事儿就交给脚本来做吧，你只需要运行，然后抽根烟的功夫就可以去下载内测包了。
*在运行次脚本之前，首先要确定功能打包没有问题，不然脚本也会打包不成功的！！！！！*
######1、将python脚本添加到当前工程的同级目录 比如：我的项目是realcast  那么python脚本的路径和realcast是在同一个目录下  他们同属于projects目录

![profile.png](http://a3.qpic.cn/psb?/V14A8Rvc2ToEea/Fq1EcCTt0Z8XIa0iKHwBEARolGI559f7Ho.nMGGvOFU!/b/dNoAAAAAAAAA&bo=7AKvAQAAAAAFAGM!&rf=viewer_4)

######2、打开终端，进入到projects目录  使用 `python ipa.py` 回车 

![terminal.png](http://a3.qpic.cn/psb?/V14A8Rvc2ToEea/dm88j0K0l9BTr5zZ11Y3v5k9TQ44S7*z8Jb8B7eAO1g!/b/dOMAAAAAAAAA&bo=ewODAAAAAAAFB98!&rf=viewer_4))





会提示你输入工程名称  例如我这里：realcast


点击回车一路往下跑,如果没有任何错误信息，那么恭喜你，自动打包成功了！  温馨提示一下：*在自动打包之前，一定要确认你工程打包能够成功，*

![result.png](http://a2.qpic.cn/psb?/V14A8Rvc2ToEea/Ajb*gASjI5OFFzQ5zSWpt*INjR4fcvYTou8H5XsQ7Qw!/b/dAwBAAAAAAAA&bo=dgNUAAAAAAAFAAI!&rf=viewer_4)

![ipapath.png](http://a2.qpic.cn/psb?/V14A8Rvc2ToEea/8v7PoE00y1pHqueRRs8OdBQFoSvbSrlJwNqnvDpmEYk!/b/dAwBAAAAAAAA&bo=AwOzAQAAAAAFAJE!&rf=viewer_4)

*在创建工程的时候千万不要用中文命名方式，切记切记！！！！！！！！！！*  此脚本我会继续维护优化，有什么问题请contact 我！！！
