*** Settings ***
# Suite Setup       GetCookies    ${url}    ${redisHost}    ${login_username}    ${login_passwd}    # cookie
# Suite Teardown    Run Keywords    Exec Sql In Mysql    ${mysqlInfo}    ${delrole}
# ...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${delrole2}
Resource          ../../../../../AutoPlatform/Interface/Public/key.robot
Resource          ../../../GlobalResource/config.robot

*** Variables ***
${rolename}       linjierole3
${new_name}       edit
${delrole}        DELETE from UPMS_ROLE where NAME='${rolename}'
${delrole2}       DELETE from UPMS_ROLE where NAME in ('${new_name}','try2','try1')

*** Test Cases ***
新增角色
    #创建角色请求
    ${roledescription}    Set variable    角色描述
    ${data}    Set variable    {"name":"${rolename}","description":"${roledescription}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/saveOrUpdateRole    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${selectrole}    Set variable    SELECT * FROM UPMS_ROLE where NAME='${rolename}'
    ${checkdict}    Set variable    {"TYPE":"0"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectrole}    ${checkdict}

修改角色
    #获取ROLE_ID
    ${ROLE_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_ROLE where NAME='${rolename}'    ROLE_ID
    ${new_descrip}    Set variable    new_descrip
    #修改角色信息
    ${data}    Set variable    {"name":"${new_name}","description":"${new_descrip}","roleId":"${ROLE_ID}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/saveOrUpdateRole    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${selectrole}    Set variable    SELECT * FROM UPMS_ROLE where NAME='${new_name}'
    ${checkdict}    Set variable    {"TYPE":"0"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectrole}    ${checkdict}

单选删除角色
    #获取ROLE_ID
    ${ROLE_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_ROLE where NAME='${new_name}'    ROLE_ID
    #单选删除角色
    ${data}    Set variable    {"roleIds":["${ROLE_ID}"]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/deleteRole    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    success    contain
    ${selectrole}    Set variable    SELECT COUNT(*) as a FROM UPMS_ROLE where NAME='${new_name}'
    ${checkdict}    Set variable    {"a":"0"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectrole}    ${checkdict}

多选删除角色
    #新增测试角色
    ${role1}    Set variable    {"name":"try1","description":"try1dd"}
    ${role2}    Set variable    {"name":"try2","description":"try2dd"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/saveOrUpdateRole    ${role1}    ${cookies}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/saveOrUpdateRole    ${role2}    ${cookies}
    #获取多角色信息
    #${ROLE_IDS}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT group_concat(ROLE_ID ORDER BY ROLE_ID SEPARATOR '","') FROM UPMS_ROLE where TYPE=0    a
    ${ROLE_ID1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_ROLE where NAME='try2'    ROLE_ID
    ${ROLE_ID2}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_ROLE where NAME='try1'    ROLE_ID
    #删除多角色
    ${data}    Set variable    {"roleIds":["${ROLE_ID1}","${ROLE_ID2}"]}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/deleteRole    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    success    contain
    ${selectrole}    Set variable    SELECT COUNT(*) as a FROM UPMS_ROLE where NAME in ('try2','try1')
    ${checkdict}    Set variable    {"a":0}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectrole}    ${checkdict}

查询全部角色
    #获取角色个数
    ${ROLE_COUNT}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT COUNT(*) as a FROM UPMS_ROLE where TENANT_ID =-1    a
    #查询角色信息
    ${data}    Set variable    {"name":"","pageIndex":1,"pageSize":10}
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/pageRoleListByName    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    "total":${ROLE_COUNT}    contain
