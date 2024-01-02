*** Settings ***
# Suite Setup       GetCookies   ${url}  ${redisHost}  ${login_username}  ${login_passwd}
Suite Teardown    Run Keywords    Exec Sql In Mysql    ${mysqlInfo}    ${delug}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${delug2}
Resource          ../../../../../AutoPlatform/Interface/Public/KEY.robot
Resource          ../../../GlobalResource/config.robot

*** Variables ***
${ug_name}        linjieug
${new_UG_NAME}    linjieug2
${delug}          DELETE from UPMS_GROUP where NAME='${ug_name}'
${delug2}         DELETE from UPMS_GROUP where NAME='${new_UG_NAME}'

*** Test Cases ***
新增用户组
    #创建用户请求
    ${ug_datail}    Set variable    linjieug_datail
    ${ug_usersql1}    Set variable    SELECT * FROM UPMS_USER order by USER_ID desc limit 1
    ${ug_usersql2}    Set variable    SELECT * FROM UPMS_USER order by USER_ID desc limit 1,1
    ${ug_user1}    Get_Data_In_Mysql    ${mysqlInfo}    ${ug_usersql1}    USER_ID
    ${ug_user2}    Get_Data_In_Mysql    ${mysqlInfo}    ${ug_usersql2}    USER_ID
    ${data}    Set variable    {"description":"${ug_datail}","name":"${ug_name}","userIdList":["${ug_user1}","${ug_user2}"]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/usergrp/save    ${data}    ${cookies}
    #检查结果
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${ug_name}'    GROUP_ID
    Check String    ${res}    ${UG_ID}    contain

添加用户时的数量校验
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${ug_name}'    GROUP_ID
    ${UserId1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER order by USER_ID desc limit 1    USER_ID
    ${UserId1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER order by USER_ID desc limit 1,1    USER_ID
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/user-cnt-check?userIdList=${UserId1},${UserId1}&groupId=    ${cookies}
    #检查结果
    Check String    ${res}    true    contain

已关联用户查询
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${ug_name}'    GROUP_ID
    ${UserId1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER order by USER_ID desc limit 1    USER_ID
    ${UserId1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER order by USER_ID desc limit 1,1    USER_ID
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/user-list?groupId=${UG_ID}    ${cookies}
    #检查结果
    Check String    ${res}    ${UserId1}    contain

编辑用户组
    #获取USER_ID
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${ug_name}'    GROUP_ID
    ${new_UG_DATAIL}    Set variable    linjieug2_detail
    ${ug_usersql}    Set variable    select * from UPMS_USER where TENANT_ID =-1 and USER_ID !=1148046988160331778 order by USER_ID limit 2,1
    ${NEW_UG_USERID}    Get_Data_In_Mysql    ${mysqlInfo}    ${ug_usersql}    USER_ID
    #修改用户信息
    ${data}    Set variable    {"groupId":"${UG_ID}","description":"${new_UG_DATAIL}","name":"${new_UG_NAME}","userIdList":["${NEW_UG_USERID}"]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/usergrp/update    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    success    contain
    ${selectug}    Set variable    SELECT * FROM UPMS_GROUP where NAME='${new_UG_NAME}'
    ${checkdict}    Set variable    {"GROUP_ID":"${UG_ID}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectug}    ${checkdict}
    ${selectug_user}    Set variable    select * from UPMS_GROUP_USER where GROUP_ID='${UG_ID}'
    ${checkdict}    Set variable    {"USER_ID":"${NEW_UG_USERID}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectug_user}    ${checkdict}

关联角色
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${new_UG_NAME}'    GROUP_ID
    #修改用户信息
    ${data}    Set variable    {"groupId": ${UG_ID},"roleIdList": [-1]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/usergrp/auth-with-role    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    success    contain

已关联角色ID列表查询
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${new_UG_NAME}'    GROUP_ID
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/role-list?groupId=${UG_ID}    ${cookies}
    #接口返回是否成功
    Check String    ${res}    200    contain
    #检查数据库
    ${role_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP_ROLE where GROUP_ID='${UG_ID}'    ROLE_ID
    Check String    ${res}    ${role_ID}    contain

导出
    #导出
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/export    ${cookies}
    #检查结果
    Check String    ${res}    P    contain

导出模板下载
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/template    ${cookies}
    #检查结果
    Check String    ${res}    P    contain

列表(返回data空)
    #列表
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/list?name=${new_UG_NAME}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

删除用户组
    #获取USER_ID
    ${UG_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_GROUP where NAME='${new_UG_NAME}'    GROUP_ID
    ${data}    Set variable    {"groupIdList":["${UG_ID}"]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/usergrp/remove    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    success    contain

查询全部用户组&重置
    #查询
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/page?pageIndex=1&pageSize=10&name=    ${cookies}
    #检查结果
    ${UG_COUNT}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT COUNT(*) as a FROM UPMS_GROUP where TENANT_ID =-1    a
    Check String    ${res}    "total":${UG_COUNT}    contain

模糊查询用户组
    #查询
    ${data}    Set variable    g
    ${res}    Http Get    ${url}    /maxs/pm/user/usergrp/page?pageIndex=1&pageSize=10&name=${data}    ${cookies}
    #检查结果
    ${UG_COUNT}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT COUNT(*) as a FROM UPMS_GROUP where TENANT_ID =-1 and NAME like '%${data}%'    a
    Check String    ${res}    "total":${UG_COUNT}    contain
