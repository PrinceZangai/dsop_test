*** Settings ***
Resource    ../../../DSOP/v3.0.1/GlobalResource/config.robot
Library    ../../../../../CustomKey/CommonLibrary/
Library    ../../../../../CustomKey/CustomLibrary/

Library    RequestsLibrary
Library    String
Library    DatabaseLibrary
Library    Collections
Library    OperatingSystem
Library    JSONLibrary


*** Variables ***


*** Keywords ***
登录    
    # ${pwd1}    Pwd Encrypt    ${pwd}
    Create Session    ${alias}    ${DSOPUrl}
    ${headers}    Create Dictionary    Accept=application/json, text/plain, */*    Content-Type=application/json;charset=UTF-8    Referer=https://${DSOPUrl}/maxPage/login    Proxy=http://localhost:8888
    # 验证码处理
    ${resp}    POST On Session    ${alias}   maxs/pm/sso/login/_isCaptcha    headers=${headers}    verify=${False}
    ${is_captcha}    Set Variable    ${{ ${resp.json()}[data] }}
    IF    ${is_captcha} == ${True}
        ${resp}    Post On Session    ${alias}    maxs/pm/sso/login/_getCaptcha    headers=${headers}    verify=${False}
        ${uuid}    Set Variable    ${resp.json()}[data][captchaUuid]
    END 
    ${pwd}    Set Variable    ${LoginPwd}
    ${pwd}    加密    ${MaxsPublicKey}    ${pwd}
    ${json}    Create Dictionary    captcha=    captchaUuid=    password=${pwd}    tenantId=-1    username=${LoginUser}
    ${response}    POST On Session    ${alias}    ${LoginUrl}    headers=${headers}    json=${json}
    ${ResponseData}    Set Variable    ${response.headers}
    ${cookies}    Get From Dictionary    ${ResponseData}    Set-Cookie
    ${cookies}    Split String    ${cookies}    ;

    ${ssa_jwt}    Split String From Right    ${cookies[3]}    ,
    ${ssa_jwt}    Set Variable    ${ssa_jwt[1]}
    ${cookies}    Set Variable    ${cookies[0]};${ssa_jwt}
    Set Global Variable    ${cookies}

登出
    ${headers}    Create Dictionary    Accept=application/json, text/plain, */*    Referer=${DSOPUrl}/maxPage/iframe    Cookie=${cookies}
    ${Response}    Get On Session    ${alias}    ${LogoutUrl}    headers=${headers}
    ${json}    Set Variable    ${Response.content}
    ${json}    to json    ${json}
    Should Be Equal As Strings    ${json}[message]    已登出
    Delete All Sessions

是否启用验证码
    ${headers}    Create Dictionary    Accept=application/json, text/plain, */*    Referer=${DSOPUrl}/maxPage/iframe
    ${url}    Set Variable    maxs/pm/sso/login/_isCaptcha
    ${resp}    Post    ${url}    headers=${headers}    verify=${False}
    [Return]    ${resp}

获取验证码
    ${headers}    Create Dictionary    Accept=application/json, text/plain, */*    Referer=${DSOPUrl}/maxPage/iframe    Cookie=${cookies}
    ${url}    Set Variable    maxs/pm/sso/login/_isCaptcha
    ${resp}    Post On Session    ${alias}    ${url}    headers=${headers}    verify=${False}
    [Return]    ${resp}

根据数据源name获取数据源id
    [Arguments]    ${name}
    ${sql}    Set Variable    select id from td_data_resource tdr where name ='${name}'
    ${result}    query    ${sql}
    [Return]    ${result}[0][0]

根据业务系统名称获取业务系统信息
    [Arguments]    ${name}
    ${result}    query    select * from `td_business_sys` where name = '${name}'    returnAsDict=True
    [Return]    ${result}[0]

根据业务系统id获取业务系统信息
    [Arguments]    ${id}
    ${result}    query    select * from `td_business_sys` where id = '${id}'    returnAsDict=True
    [Return]    ${result}[0]

根据数据源名称获取数据源信息
    [Arguments]    ${name}
    ${result}    query    select * from `td_data_resource` where name = '${name}'    returnAsDict=True
    [Return]    ${result}[0]

根据名称获取id
    [Arguments]    ${name}    ${db}    ${table}    ${other}=
    [Documentation]    ${name}实体名称，数据源名称、识别任务名称等    ${db}数据库名    
    ...    ${table}表名    ${other}其他sql条件，会被拼接在语句最后面
    ${sql}    Set Variable    select id from ${db}.${table} where name='${name}' ${other}
    ${result}    Query    ${sql}
    [Return]    ${result}

根据名称获取数据
    [Arguments]    ${name}    ${db}    ${table}    ${other}=
    [Documentation]    ${name}实体名称，数据源名称、识别任务名称等    ${db}数据库名    
    ...    ${table}表名    ${other}其他sql条件，会被拼接在语句最后面    
    ${sql}    Set Variable    select * from ${db}.${table} where name='${name}' ${other}
    ${result}    Query    ${sql}
    [Return]    ${result}

请求
    [Arguments]    ${url}    ${method}    &{kwargs}
    ${headers}    create header
    # 处理headers，如果kwargs中包含headers
    ${key_exists}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${kwargs}    headers
    IF    ${key_exists}==${False}
        Set To Dictionary    ${kwargs}    headers=${headers}    
    END
    ${url}    Set Variable    ${DSOPUrl}${url}
    ${resp}    通用请求    ${url}    ${method}    &{kwargs}
    [Return]    ${resp.json()}

请求-返回Response
    [Arguments]    ${url}    ${method}    &{kwargs}
    ${headers}    create header
    # 处理headers，如果kwargs中包含headers
    ${key_exists}=    Run Keyword And Return Status    Dictionary Should Contain Key    ${kwargs}    headers
    IF    ${key_exists}==${False}
        Set To Dictionary    ${kwargs}    headers=${headers}    
    END
    ${url}    Set Variable    ${DSOPUrl}${url}
    ${resp}    通用请求    ${url}    ${method}    &{kwargs}
    [Return]    ${resp}

create header
    ${headers}    Create Dictionary    Accept=application/json, text/plain, */*    Cookie=${cookies}
    [Return]    ${headers}

set project path
    ${projectPath}    Evaluate    os.getcwd()
    Set Global Variable    ${projectPath}
    # log to console    ${projectPath}

set testFile path
    ${testFilePath}    Set Variable    ${projectPath}/测试工程/DSOP_project/DSOP/v3.0.1/GlobalResource/TestFiles
    Set Global Variable    ${testFilePath}

连接DC_MySql
    ${host}    Set Variable    ${MySQL配置}[0]
    ${port}    Set Variable    ${MySQL配置}[1]
    ${user}    Set Variable    ${MySQL配置}[2]
    ${passwd}    Set Variable    ${MySQL配置}[3]
    Connect To Database Using Custom Params    pymysql    host='${host}', port=${port}, user='${user}', passwd='${passwd}', db='${DC_db}', charset='utf8'

连接MAXs_MySql
    ${host}    Set Variable    ${MySQL配置}[0]
    ${port}    Set Variable    ${MySQL配置}[1]
    ${user}    Set Variable    ${MySQL配置}[2]
    ${passwd}    Set Variable    ${MySQL配置}[3]
    Connect To Database Using Custom Params    pymysql    host='${host}', port=${port}, user='${user}', passwd='${passwd}', db='${Maxs_DB}', charset='utf8'

断开数据库
    Disconnect From Database

# GetCookies
#     [Arguments]    ${url}    ${host}    ${user}     ${pwd}    # 参数1为url；参数2为访问路径；参数3为post数据。
#     [Documentation]    \# 参数1为url；参数2为访问路径；参数3为post数据。
#     ${cookies}    getLoginCookies    ${url}    ${host}    ${user}     ${pwd}
#     Set Global Variable    ${cookies}    ${cookies}