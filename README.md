AISDSOPV1.0自动化测试脚本
2023-07-18

# 环境
python==3.7.9
其他依赖位于根目录中的requirement.txt

一键导入依赖
```shell
pip install -r requirements.txt
```
# 项目结构说明  
│  AISDC1.0自动化功能清单.xlsx  
│  README.md  
│  requirements.txt #项目依赖  
│  __init__.txt  
└─project-AISDC  
    │  __init__.py  
    │  项目配置参数-DC.txt #项目配置文件  
    ├─Automation关键字  
    ├─Data #用例数据文件夹  
    ├─Resources #项目资源文件夹，自定义关键字导入位置  
    └─测试模块-HTTP接口 #项目用例文件夹，执行用例  
        └─04.数据资产中心  
            └─数据源管理  
                │  关键字.robot    #模块关键字，单接口请求位于此处  
                │  变量.robot     #模块变量文件  
                │  测试集.robot    #模块用例  
                └─results #用例运行报告文件夹，只会存放单次用例报告  

# 运行  
## 命令行运行 
cd 到项目根目录  
### 按用例名称执行
```shell
robot -d results -t 新增mysql数据源 -P .\project-AISDC\Resources ./  
```
![img_2.png](images/img_2.png)
### 执行所有用例
```shell
robot -d results -P .\project-AISDC\Resources ./  
```
![img_1.png](images/img_1.png)
### 参数说明
    -d 指定用例报告位置  
    -t 指定用例名称，不给则执行目录下所用用例  
    -P 指定项目资源寻找位置，必须指定为项目资源目录，否则找不到关键字
    ./ 在此目录下寻找用例
### 查看更多参数  
```shell
robot --help
```

# ide工具

## vscode（推荐）

![](D:\personal data\programs\AISDSOP_AutoTest\image-20231215143400476.png)

## pycharm运行

下载插件

![image-20230907154408795](images/image-20230907154408795.png)

![image-20230907154703227](images/image-20230907154703227.png)

###  配置robot运行脚本

打开pycharm，点击“File-Settings-Tools-External Tools”

![image-20230907154831677](images/image-20230907154831677.png)

#### 单用例运行配置

点击“+”进行新增tool，依次输入下面几个参数：

Name：Robot Run SingleTestCase

Program：你自己的robot.exe所在位置（例如：D:\Python\Python37\Scripts\robot.exe)

Arguments：-d results   -P .\project-AISDC\Resources -t "$SelectedText$" ./

Working directory：你的项目根目录(例如：D:\download\DC_TESTCASES)

![image-20230907145727393](images/image-20230907145727393.png)

#### 测试套运行配置

点击“+”进行新增tool，依次输入下面几个参数：

Name：Robot Run TestSuite

Program：你自己的robot.exe所在位置（例如：D:\Python\Python37\Scripts\robot.exe)

Arguments：-d results -P .\project-AISDC\Resources  $FileName$

Working directory：你的项目根目录(例如：D:\download\DC_TESTCASES)

![image-20230907145955485](images/image-20230907145955485.png)

单用例运行步骤：

选中用例名称->右键->External tools->Run Robot SingleCase

![image-20230907150250305](images/image-20230907150250305.png)

![image-20230907150220539](images/image-20230907150220539.png)

![image-20230907150511903](images/image-20230907150511903.png)

多用例运行步骤：

选中文件夹->右键->External tools->Run Robot TestSuite

![image-20230907150744373](images/image-20230907150744373.png)

运行效果

![image-20230907150851614](images/image-20230907150851614.png)

## ride运行

设置运行参数->选中用例->运行

![image-20230907152439283](images/image-20230907152439283.png)

![image-20230907152545790](images/image-20230907152545790.png)
