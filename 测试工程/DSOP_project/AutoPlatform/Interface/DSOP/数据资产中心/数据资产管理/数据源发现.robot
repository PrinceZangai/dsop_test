*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections

*** Variables ***
${addDataResourceProbe_url}      /dc-manager/api/dataResourceProbe/add
${deleteDataResourceProbe_url}      /dc-manager/api/dataResourceProbe/batchDeleteJob
${stopDataResourceProbe_url}      /dc-manager/api/dataResourceProbe/stopJob

*** Keywords ***
新增数据源发现_单次执行
    [Arguments]     ${jobMode}=1    ${portScope}=8080,1521,3306,21,22,1433    ${name}=1    ${portType}=1   ${ipArr}=127.0.0.1    ${jobType}=1    ${whiteList}=127.0.0.1   ${startIp}=1.1.1.1    ${endIp}=1.1.1.1      ${cycleConfig}={}
    ...    ${cron}=''   ${dateTime}=''      ${cycleType}=null    ${resPoolId}=1
    ${ipScopeString}    set variable    [{"startIp":"${startIp}","endIp":"${endIp}"}]
    ${day}    create list
    ${week}    create list
    ${year}    create list
    ${cycleConfig}      create dictionary    cron=${cron}   dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    ${json}    create dictionary    jobMode=${jobMode}    portScope=${portScope}   name=${name}     portType=${portType}    ipArr=${ipArr}      jobType=${jobType}    whiteList=${whiteList}    ipScope=${ipScopeString}    cycleConfig=${cycleConfig}      resPoolId=${resPoolId}
    ${resp}    请求    ${addDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

新增数据源发现_执行一次
    [Arguments]     ${jobMode}=1    ${portScope}=8080,1521,3306,21,22,1433      ${jobType}=2    ${dateTime1}=2023-12-10T16:00:00.000Z     ${dateTime11}=2023-12-12T13:14:52.000Z    ${name}=1
    ...    ${startIp}=1.1.1.1    ${endIp}=1.1.1.1      ${cycleConfig}={}   ${portType}=1    ${resPoolId}=1    ${cron}=      ${dateTime}=2023-12-12 14:52:53     ${cycleType}=1
    ${ipScopeString}    set variable    [{"startIp":"${startIp}","endIp":"${endIp}"}]
    ${day}    create list
    ${week}    create list
    ${year}    create list
    ${cycleConfig}      create dictionary    cron=${cron}   dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    ${json}    create dictionary    jobMode=${jobMode}    portScope=${portScope}   jobType=${jobType}    dateTime1=${dateTime1}    dateTime11=${dateTime11}    name=${name}     ipScope=${ipScopeString}
    ...    cycleConfig=${cycleConfig}    portType=${portType}      resPoolId=${cycleType}
    ${resp}    请求    ${addDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

新增数据源发现_每天执行
    [Arguments]     ${jobMode}=2    ${portScope}=8080,1521,3306,21,22,1433      ${jobType}=2    ${dateTime2}='2023-11-24T06:48:02.000Z'    ${name}=1      ${cycleConfig}={}
    ...    ${startIp}=1.1.1.1    ${endIp}=1.1.1.1   ${portType}=1    ${resPoolId}=1    ${cron}=''      ${dateTime}=2023-11-24 14:52:53     ${cycleType}=2
    ${ipScopeString}    set variable    [{"startIp":"${startIp}","endIp":"${endIp}"}]
    ${day}    create list
    ${week}    create list
    ${year}    create list
    ${cycleConfig}      create dictionary    cron=${cron}   dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    ${json}    create dictionary    jobMode=${jobMode}    portScope=${portScope}   jobType=${jobType}    dateTime2=${dateTime2}    name=${name}     ipScope=${ipScopeString}
    ...    cycleConfig=${cycleConfig}    portType=${portType}      resPoolId=${resPoolId}
    ${resp}    请求    ${addDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

新增数据源发现_每周执行
    [Arguments]     ${jobMode}=3    ${portScope}=8080,1521,3306,21,22,1433      ${jobType}=2    ${dateTime3}='2023-11-24T03:07:37.000Z'    ${name}=1      ${week1}=1    ${ipArr}=127.0.0.1
    ...     ${whiteList}=127.0.0.1    ${cycleConfig}={}    ${startIp}=1.1.1.1    ${endIp}=1.1.1.1   ${portType}=1    ${resPoolId}=1    ${cron}=''      ${dateTime}=2023-11-24 14:52:53     ${cycleType}=3
    ${ipScopeString}    set variable    [{"startIp":"${startIp}","endIp":"${endIp}"}]
    ${day}    create list
    ${week}    create list
    ${int_week1}    Convert To Integer    ${week1}
    Append To List    ${week}    ${int_week1}
    ${year}    create list
    ${cycleConfig}      create dictionary    cron=${cron}   dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    ${json}    create dictionary    jobMode=${jobMode}    portScope=${portScope}    name=${name}   jobType=${jobType}    dateTime3=${dateTime3}     week=${week1}    ipArr=${ipArr}    whiteList=${whiteList}
    ...    ipScope=${ipScopeString}    cycleConfig=${cycleConfig}    portType=${portType}      resPoolId=${resPoolId}
    ${resp}    请求    ${addDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

新增数据源发现_每月执行
    [Arguments]     ${jobMode}=4    ${portScope}=8080,1521,3306,21,22,1433      ${jobType}=2    ${dateTime4}='2023-11-24T06:50:02.000Z'    ${name}=1      ${day1}=1
    ...    ${cycleConfig}={}    ${startIp}=1.1.1.1    ${endIp}=1.1.1.1   ${portType}=1    ${resPoolId}=1    ${cron}=''      ${dateTime}=2023-11-24 14:50:02     ${cycleType}=4
    ${ipScopeString}    set variable    [{"startIp":"${startIp}","endIp":"${endIp}"}]
    ${day}    create list
    ${int_day1}    Convert To Integer    ${day1}
    Append To List    ${day}    ${int_day1}
    ${week}    create list
    ${year}    create list
    ${cycleConfig}      create dictionary    cron=${cron}   dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    ${json}    create dictionary    jobMode=${jobMode}    portScope=${portScope}   jobType=${jobType}    dateTime4=${dateTime4}      day=${day1}   name=${name}
    ...    ipScope=${ipScopeString}    cycleConfig=${cycleConfig}    portType=${portType}      resPoolId=${resPoolId}
    ${resp}    请求    ${addDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

获取数据源发现任务的id
    [Arguments]    ${name}
    # \ \ \ 通过识别模板名称获取数据源id，以备后续建扫描任务时需要
    连接MySql
    ${sql}    set variable    select id from td_data_source_discovery_job tdr where name ='${name}' order by id desc
    ${result}    query    ${sql}
    [Return]    ${result}[0][0]

停止数据源发现任务
    [Arguments]    ${id}=25    ${resPoolId}=1
    ${json}    create dictionary    resPoolId=${resPoolId}      id=${id}
    ${resp}    请求    ${stopDataResourceProbe_url}    POST    json=${json}
    [Return]    ${resp}

删除数据源发现
    [Arguments]     ${name}=每月执行
#   根据name获取要删除的任务id
    ${resp}    获取数据源发现任务的id     name=${name}
#    删除前先停止数据源发现任务
    ${resp-stop}    停止数据源发现任务     id=${resp}
    should be equal as strings    终止数据源探测任务成功!    ${resp-stop}[msg]
#    根据获取的id删除数据源
    ${idsList}    create list
    ${int_ids}    Convert To Integer    ${resp}
    Append To List    ${idsList}      ${int_ids}
    ${json}    create dictionary    ids=${idsList}
    ${resp}    请求    ${deleteDataResourceProbe_url}    DELETE    json=${json}
    [Return]    ${resp}