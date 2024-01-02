*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/

*** Variables ***
${addAccessDevice_url}    /data-access/quickCreate/addAccessDevice
${getAllPort_url}    /data-access/quickCreate/getAllPort
${getAllCreate_url}    /data-access/quickCreate/getAllCreate
${getHostByType_url}    /data-access/hostmanager/getHostByType
${createFlume_url}    /data-access/flume/create
${startFlume_url}    /data-access/flume/start
${createTaskByOneKeyCreate_url}    /data-access/process/pipeline/createTaskByOneKeyCreate
${startTask_url}    /data-access/process/pipeline/start/INS_17038192455103172

*** Keywords ***
新增采集
    [Arguments]    ${topic}    ${name}    ${config}    ${type}=0    ${partition}=1    ${replica}=1    ${remark}=""
    [Documentation]    ${type}flume类型,0:udp,4:floder    ${topic}kafka topic    ${name}采集名称
    ...    ${partition}分区数    ${replica}副本数    ${config}配置，跟type相关    ${remark}描述
    ${request_json}    Create Dictionary    type=${type}    topic=${topic}    name=${name}    partition=${partition}    replica=${replica}    config=${config}    remark=${remark}
    ${resp}    请求    ${createFlume_url}    POST    json=${request_json}
    [Return]    ${resp}

启动采集
    [Arguments]    ${id}    
    ${request_json}    Create Dictionary    id=${id}
    ${resp}    请求    ${startFlume_url}    POST    json=${request_json}
    [Return]    ${resp}

启动预处理任务
    [Arguments]    ${code}
    ${resp}    请求    ${startTask_url}/${code}    POST   
    [Return]    ${resp}

根据类型获取主机
    [Arguments]    ${clusterType}
    ${request_json}    Create Dictionary    clusterType=${clusterType}
    ${resp}    请求    ${getHostByType_url}    POST    json=${request_json}
    [Return]    ${resp}

查询所有设备
    [Arguments]    ${type}
    [Documentation]
    ${request_json}    Create Dictionary    type=${type}
    ${resp}    请求    ${getAllCreate_url}    POST    json=${request_json}
    [Return]    ${resp}
    
一键接入新增任务
    [Arguments]    ${name}    ${spiderId}    ${ruleId}    ${desc}=""
    [Documentation]
    ${request_json}    Create Dictionary    name=${name}    spiderId=${spiderId}    ruleId=${ruleId}    desc=${desc}
    ${resp}    请求    ${createFlume_url}    POST    json=${request_json}
    [Return]    ${resp}
