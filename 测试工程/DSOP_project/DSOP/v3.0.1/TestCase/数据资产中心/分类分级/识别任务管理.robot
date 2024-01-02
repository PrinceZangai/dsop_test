*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/分类分级/识别任务管理.robot
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/数据资产管理/数据源管理.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/


*** Test Cases ***
新增默认模板扫描任务
    [Tags]    @author=wang.shu   @runlevel=smoke    @priority=P0
    ${timestamp}    get current timestamp
    ${db_info}    get dictionary from file    ${projectPath}/测试工程/DSOP_project/DSOP/v3.0.1/GlobalResource/TestFiles/databases.yaml
    ${mysql_info}    set variable    ${db_info}[识别任务数据源]
    ${timestamp}    get current timestamp
    ${dataSourceName}    Set Variable    自动化测试-识别任务模板数据源
    ${resp}    新增数据源    ${dataSourceName}    ${mysql_info}[ipPortList]    ${mysql_info}[user]    ${mysql_info}[password]    ${mysql_info}[versionName]    serverPath=${mysql_info}[serverPath]
    
    ${dataSourceId}    获取数据源id    ${dataSourceName}
    ${templateId}    获取识别模板id    公共行业数据分类分级标准
    ${taskName}    Set Variable    自动化测试-识别任务
    ${resp}    新增扫描任务    name=${taskName}    dataSourceId=${dataSourceId}    templateId=${templateId}
    should be equal as strings    任务新增成功    ${resp}[msg]
    
稽核
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    自动化测试-识别任务
    ${templateId}    获取识别模板id    公共行业数据分类分级标准
    ${sql}    Set Variable    SELECT id,status FROM td_data_recognition_job WHERE name='${name}';
    ${result}    query    ${sql}
    # 轮询数据库，由于mysql隔离级别问题，必须重新连接
    WHILE    ${result}[0][1]!=4    limit=40s
        断开数据库
        连接MySql
        ${result}    query    ${sql}
        Sleep    2
    END
    ${jobId}    Convert To String    ${result}[0][0]
    ${resp}    稽核    ${jobId}    ${templateId}
    Should Be Equal As Strings    识别结果稽核成功    ${resp}[msg]

查看任务详情
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${name}    Set Variable    自动化测试-识别任务
    ${result}    根据名称获取id    ${name}    ${DC_db}    td_data_recognition_job
    ${resp}    查看识别任务详情    ${result}[0][0]
    Should Be Equal As Strings    操作成功    ${resp}[msg]

删除识别任务
    ${name}    Set Variable    自动化测试-识别任务
    ${sql}    Set Variable    SELECT id,status FROM td_data_recognition_job WHERE name='${name}';
    ${result}    query    ${sql}
    ${jobId}    Convert To String    ${result}[0][0]
    ${resp}    删除识别任务    ${jobId}
    Should Be Equal As Strings    任务删除成功    ${resp}[msg]

# 新增识别任务-稽核-查看详情-删除任务
#     [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
#     ${timestamp}    get current timestamp
#     ${name}    Set Variable    新增扫描任务-${timestamp}
#     Log To Console    ${name}
#     ${dataSourceId}    获取数据源id    批量导入mysql_134
#     Log To Console    ${dataSourceId}
#     ${templateId}    获取识别模板id    公共行业数据分类分级标准
#     Log To Console    ${templateId}
#     ${resp}    新增扫描任务    name=${name}    dataSourceId=${dataSourceId}    templateId=${templateId}
#     Log To Console    ${resp}
#     should be equal as strings    任务新增成功    ${resp}[msg]
    
#     ${sql}    Set Variable    SELECT id,status FROM aisdss.td_data_recognition_job WHERE name='${name}';
#     ${result}    query    ${sql}
#     # 轮询数据库，由于mysql隔离级别问题，必须重新连接
#     WHILE    ${result}[0][1]!=4    limit=40s
#         断开数据库
#         连接MySql
#         ${result}    query    ${sql}
#         Sleep    2
#     END
#     ${jobId}    Convert To String    ${result}[0][0]
#     ${resp}    稽核    ${jobId}    ${templateId}
#     Should Be Equal As Strings    识别结果稽核成功    ${resp}[msg]

#     ${resp}    查看识别任务详情    ${jobId}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]
#     # TODO 待校验
    
#     ${resp}    删除识别任务    ${jobId}
#     Should Be Equal As Strings    任务删除成功    ${resp}[msg]

