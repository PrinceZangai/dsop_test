*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/数据资产管理/业务系统管理.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/

*** Test Cases ***
新增-删除业务系统
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    自动化测试-新增业务系统
    ${deptList}    Set Variable    ${{ [{"deptId": "1", "deptName": "全部"}] }}
    ${owner}    Set Variable    admin
    ${ownerId}    Set Variable    1
    ${ipArea}    Set Variable    10.21.20.10
    ${resp}    新增业务系统    ${name}    ${deptList}    ${ownerId}    ${owner}    ${ipArea}
    Should Be Equal As Strings    新增业务系统成功    ${resp}[msg]
    
    ${result}    Query    select id,name from td_business_sys where name='${name}' and del_flag=0;
    ${ids}    Create List    ${{ ${result}[0][0] }}
    ${resp}    删除业务系统    ${ids}
    Should Be Equal As Strings    批量删除业务系统成功    ${resp}[msg]

分页查询业务系统
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${resp}    分页查询业务系统
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    
    ${data}    Set Variable    ${resp}[data][list]
    ${assertColumns}    Create List    id    name    ipArea    owner    
    ${data_from_resp}     Get Data From Datalist    ${data}    ${assertColumns}
    ${default_bus}    Remove From List    ${data_from_resp}    0
    ${sql}    Set Variable     select id,name,ip_area,owner,dept_list from td_business_sys tbs where del_flag=0 and name!='默认业务系统' order by create_time desc limit 0,9;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 4))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}    
    Lists Should Be Equal    ${data_from_resp}    ${data_from_sqlresult}
