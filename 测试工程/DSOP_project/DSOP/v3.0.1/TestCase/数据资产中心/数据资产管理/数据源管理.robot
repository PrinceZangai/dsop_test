*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/数据资产管理/数据源管理.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/

*** Test Cases ***
新增mysql数据源
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${db_info}    get dictionary from file    ${projectPath}/测试工程/DSOP_project/DSOP/v3.0.1/GlobalResource/TestFiles/databases.yaml
    ${mysql_info}    set variable    ${db_info}[mysql]
    ${timestamp}    get current timestamp
    ${name}    Set Variable    自动化测试-新增数据源
    ${db_pwd}    加密    ${DCPublicKey}    ${mysql_info}[password]
    ${resp}    新增数据源    ${name}    ${mysql_info}[ipPortList]    ${mysql_info}[user]    ${db_pwd}    ${mysql_info}[versionName]
    should be equal as strings    新增数据源成功    ${resp}[msg]

查看数据源详情
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    自动化测试-新增数据源
    ${resp}    查询数据源详情    ${name}
    ${result}    查询数据源详情-数据库    ${name}
    Compare Dicts    ${resp}    ${result}
    
分页查询数据源-默认参数
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${resp}    分页查询数据源
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    ${assertColumns}    Create List    name    connectStatusDesc    isClusterDesc    serverPath    owner   
    ${data_from_resp}    Get Data From Datalist    ${resp}[data][list]    ${assertColumns}
    ${sql}    Set Variable    select name,if(connect_status=1,'未连接',if(connect_status=2,'已连接','连接失败')),if(is_cluster=1,'是','否'),server_path,owner from td_data_resource tdr order by create_time desc limit 0,10;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 5))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}

删除mysql数据源
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    自动化测试-新增数据源
    ${resp}    删除数据源    ${name}
    Should Be Equal As Strings    删除数据源成功    ${resp}[msg]

分页查询未知数据源-默认参数
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${resp}    分页查询未知数据源
    ${resp_db}     分页查询未知数据源-业务库查询
    Lists Should Be Equal    ${resp}    ${resp_db}

未知数据源补全-删除-SFTP
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    补全-sftp
    ${resp}     未知数据源补全-sftp    name=${name}    ip=10.21.171.140     port=22    typeName=SFTP    serverPath=/home     userName=aidm
    ...     password=8uhb*UHB      businessName=默认业务系统
    Should Be Equal As Strings    补全数据源成功    ${resp}[msg]
    ${resp}    删除数据源    name=${name}
    Should Be Equal As Strings    删除数据源成功    ${resp}[msg]

未知数据源补全-删除-DATABASE
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    补全-database
    ${resp}     未知数据源补全-database    name=${name}    ip=10.21.171.140     port=3306    typeName=MySQL    versionName=5.x      serverPath=prod     userName=aidm
    ...     password=8uhb*UHB
    Should Be Equal As Strings    补全数据源成功    ${resp}[msg]
    ${resp}    删除数据源    name=${name}
    Should Be Equal As Strings    删除数据源成功    ${resp}[msg]

