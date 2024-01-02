*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/平台管理/数据接入/一键接入.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/

*** Test Cases ***
接入设备-数据库审计
    ${resp}    根据类型获取主机    clusterType=0
    ${host_info}    Set Variable    ${resp}[0]
    ${resp}    查询所有设备    -1
    ${device_info}    Set Variable    ${resp}[data][0]    
    ${name}    Set Variable    ${device_info}[DEVICE_TYPE]
    ${deviceId}    Set Variable    1
    ${random1}    Get Date    days    0    %Y%m%d%H%M%S%f
    ${topic}    Set variable    MAXS_COLLECT_${random1}
    ${charset}    Set Variable    "UTF-8"
    ${clusterType}    Set Variable    0
    ${config}    Convert String To Dictionary    {"charset": ${charset},"clusterType": ${clusterType},"deviceId":${device_info}[ID] ,"host": ${host_info}[id],"port": ${device_info}[PORT_DEFAULT],"visitIp": ""}
    ${resp}    新增采集    ${topic}    ${name}    ${config}
    Should Be Equal As Strings    保存成功    ${resp}[message]
    # 一键接入新增预处理任务
    ${ruleId}    Evaluate    json.loads('${device_info}[DATAPROCESS_CONFIG]')['ruleId']
    ${flume_id}    Set Variable    ${resp}[data]
    ${resp}    一键接入新增任务    ${name}    ${flume_id}    ${ruleId}
    Should Be Equal As Strings    保存成功    ${resp}[message]
    ${code}    Set Variable    ${resp}[data]
    # 启动采集
    ${resp}    启动采集    ${flume_id}
    Should Be Equal As Strings    启用成功    ${resp}[message]
    # 启动预处理任务
    ${resp}    启动预处理任务    ${code}
    Should Be Equal As Strings    创建成功    ${resp}[message]

接入设备-文件防泄露
    ${resp}    根据类型获取主机    clusterType=0
    ${host_info}    Set Variable    ${resp}[3]
    ${resp}    查询所有设备    -1
    ${device_info}    Set Variable    ${resp}[data][0]    
    ${name}    Set Variable    ${device_info}[DEVICE_TYPE]
    ${deviceId}    Set Variable    1
    ${random1}    Get Date    days    0    %Y%m%d%H%M%S%f
    ${topic}    Set variable    MAXS_COLLECT_${random1}
    ${charset}    Set Variable    "UTF-8"
    ${clusterType}    Set Variable    0
    ${config}    Convert String To Dictionary    {"charset": ${charset},"clusterType": ${clusterType},"deviceId":${device_info}[ID] ,"host": ${host_info}[id],"port": ${device_info}[PORT_DEFAULT],"visitIp": ""}
    ${resp}    新增采集    ${topic}    ${name}    ${config}
    Should Be Equal As Strings    保存成功    ${resp}[message]
    # 一键接入新增预处理任务
    ${ruleId}    Evaluate    json.loads('${device_info}[DATAPROCESS_CONFIG]')['ruleId']
    ${flume_id}    Set Variable    ${resp}[data]
    ${resp}    一键接入新增任务    ${name}    ${flume_id}    ${ruleId}
    Should Be Equal As Strings    保存成功    ${resp}[message]
    ${code}    Set Variable    ${resp}[data]
    # 启动采集
    ${resp}    启动采集    ${flume_id}
    Should Be Equal As Strings    启用成功    ${resp}[message]
    # 启动预处理任务
    ${resp}    启动预处理任务    ${code}
    Should Be Equal As Strings    创建成功    ${resp}[message]


test
    ${resp}    查询所有设备    -1
    ${device_info}    Set Variable    ${resp}[data][0]    
    ${ruleId}    Evaluate    json.loads('${device_info}[DATAPROCESS_CONFIG]')['ruleId']

    log to console    mess

