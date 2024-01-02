*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/数据资产管理/数据源发现.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/


*** Test Cases ***
新增数据源发现_单次执行
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    单次执行
    ${resp}    新增数据源发现_单次执行      name=${name}      startIp=10.21.171.139       endIp=10.21.171.140
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]


新增数据源发现_执行一次
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    执行一次
    ${dateTime}    Get Current Time
    ${resp}    新增数据源发现_执行一次      name=${name}      
    ...    startIp=10.21.171.139       endIp=10.21.171.140    dateTime=${dateTime}
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]


新增数据源发现_每天执行
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    每天执行
    ${resp}    新增数据源发现_每天执行      name=${name}      startIp=10.21.171.139       endIp=10.21.171.140
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]


新增数据源发现_每周执行
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    每周执行
    ${resp}    新增数据源发现_每周执行      name=${name}      startIp=10.21.171.139       endIp=10.21.171.140
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]

新增数据源发现_每月执行
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    每月执行
    ${resp}    新增数据源发现_每月执行      name=${name}      startIp=10.21.171.139       endIp=10.21.171.140
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]

删除数据源发现
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    每天执行-删除
    ${resp}    新增数据源发现_每天执行      name=${name}      startIp=10.21.171.139       endIp=10.21.171.140
    Log To Console    ${resp}
    should be equal as strings    新增/复制数据源探测任务成功    ${resp}[msg]
    ${resp}    删除数据源发现      name=${name}
    Log To Console    ${resp}
    should be equal as strings    批量删除成功     ${resp}[msg]