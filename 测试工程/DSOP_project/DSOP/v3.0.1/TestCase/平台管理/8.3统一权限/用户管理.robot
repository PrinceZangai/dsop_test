*** Settings ***
# Suite Setup       GetCookies    ${url}    ${redisHost}    ${login_username}    ${login_passwd}
Suite Teardown    Run Keywords    Exec Sql In Mysql    ${mysqlInfo}    ${delrole}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${deluser}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${delrole2}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${deluser2}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${delrole3}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${deluser3}
Resource          ../../../../../AutoPlatform/Interface/Public/key.robot
Resource          ../../../GlobalResource/config.robot

*** Variables ***
${username}       ljtest1
${username2}      ljtest2
${delrole}        DELETE from UPMS_USER_ROLE where USER_ID in (SELECT user_id FROM UPMS_USER where username='${username}')
${deluser}        DELETE FROM UPMS_USER where    username='${username}'
${delrole2}       DELETE from UPMS_USER_ROLE where USER_ID in (SELECT user_id FROM UPMS_USER where username='${username2}')
${deluser2}       DELETE FROM UPMS_USER where    username='${username2}'
${delrole3}       DELETE from UPMS_USER_ROLE where USER_ID in (SELECT user_id FROM UPMS_USER where username='test101')
${deluser3}       DELETE FROM UPMS_USER where    username='test101'

*** Test Cases ***
_getAvatar
    ${res}    HttpGet    ${url}    /maxs/pm/user/userCfg/_getAvatar    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

用户授权
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_USER_ROLE uur where USER_ID =(select USER_ID from UPMS_USER where USERNAME='${login_username}')    USER_ID
    ${role_ID}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_USER_ROLE uur where USER_ID =(select USER_ID from UPMS_USER where USERNAME='${login_username}')    ROLE_ID
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/authUser    {"roleIds": [${role_ID}],"sourceType": 0,"userId": ${USER_ID}}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

用户列表
    ${data}    Set variable    {"pageSize":10,"pageIndex":1,"name":"","username":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/listMaxsUser    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

分页用户列表
    ${data}    Set variable    {"pageSize":10,"pageIndex":1,"name":"","username":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/pageMaxsUser    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

用户模板下载
    ${res}    HttpGet    ${url}    /maxs/pm/user/userCfg/downTemplate    ${cookies}
    #检查结果
    Check String    ${res}    P    contain

用户名查重
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/checkUserName    {"username": "${login_username}"}    ${cookies}
    #检查结果
    Check String    ${res}    已存在相同用户登录名    contain

新增用户
    #创建用户请求
    ${phone}    Set variable    15915915911
    ${email}    Set variable    1%401.com
    ${email_utf8}    Set variable    1@1.com
    ${data}    Set variable    {"username":"${username}","name":"${username}","orgIds":[1],"gender":"1","email":"${email_utf8}","phone":"${phone}","avatar":""}
    ${res}    HttpPost    ${url}    maxs/pm/user/userCfg/saveUser    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${selectuser}    Set variable    SELECT * FROM UPMS_USER where username='${username}'
    ${checkdict}    Set variable    {"STATUS":"1","PHONE":"${phone}","EMAIL":"${email_utf8}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectuser}    ${checkdict}

修改用户密码
    ${newpwd}    Pwd Encrypt    123456
    ${data}    Set variable    {"newPwd":"${newpwd}","oldPwd":"${newpwd}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/editPwd    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain

修改用户
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${new_phone}    Set variable    13813813811
    ${new_email}    Set variable    2%402.com
    ${new_email_utf8}    Set variable    2@2.com
    #修改用户信息
    ${data}    Set variable    {"userId":"${USER_ID}","username":"${username}","name":"${username}","orgIds":[1],"gender":"1","email":"${new_email_utf8}","phone":"${new_phone}","avatar":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/updateUser    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    操作成功    contain
    ${selectuser}    Set variable    SELECT * FROM UPMS_USER where username='${username}'
    ${checkdict}    Set variable    {"STATUS":"1","PHONE":"${new_phone}","EMAIL":"${new_email_utf8}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${selectuser}    ${checkdict}

listOrgByUserId
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    {"userId":${USER_ID}}
    #发送请求
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/listOrgByUserId    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

listRoleByUserId
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    {"userId":${USER_ID}}
    #发送请求
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/listRoleByUserId    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

锁定
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    {"userId":${USER_ID}}
    #发送请求
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/lock    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    成功    contain

解锁
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    {"userId":${USER_ID}}
    #发送请求
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/unlock    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    成功    contain

生成密钥
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    userId=${USER_ID}
    #生成密钥
    ${res}    HttpGet    ${url}    /maxs/pm/authority/userCfg/generateKey.do?${data}    ${cookies}
    #检查结果
    Check String    ${res}    密钥生成成功    contain
    ${PUBLIC_KEY}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT PUBLIC_KEY FROM UPMS_USER where user_id = '${USER_ID}'    PUBLIC_KEY
    Check String    ${res}    ${PUBLIC_KEY}    contain

获取密钥
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    ${data}    Set variable    userId=${USER_ID}
    #获取密钥
    ${res}    HttpGet    ${url}    /maxs/pm/authority/userCfg/getKeyByUserId.do?${data}    ${cookies}
    #检查结果
    Check String    ${res}    获取密钥成功    contain
    ${PUBLIC_KEY}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT PUBLIC_KEY FROM UPMS_USER where user_id = '${USER_ID}'    PUBLIC_KEY
    Check String    ${res}    ${PUBLIC_KEY}    contain

单个删除用户
    #获取USER_ID
    ${USER_ID}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username}'    USER_ID
    #修改用户信息
    ${data}    Set variable    {"userId":"${USER_ID}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/delUser    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    删除用户成功    contain

批量删除用户
    #创建测试用户2
    ${phone}    Set variable    15915915912
    ${email}    Set variable    1%401.com
    ${email_utf8}    Set variable    1@2.com
    ${data}    Set variable    {"username":"${username2}","name":"${username2}","orgIds":[1],"gender":"1","email":"${email_utf8}","phone":"${phone}","avatar":""}
    ${res}    HttpPost    ${url}    maxs/pm/user/userCfg/saveUser    ${data}    ${cookies}
    #检查创建结果2
    Check String    ${res}    true    contain
    #创建测试用户3
    ${username3}    Set variable    ljtest3
    ${phone}    Set variable    15915915913
    ${email}    Set variable    1%401.com
    ${email_utf8}    Set variable    1@3.com
    ${data}    Set variable    {"username":"${username3}","name":"${username3}","orgIds":[1],"gender":"1","email":"${email_utf8}","phone":"${phone}","avatar":""}
    ${res}    HttpPost    ${url}    maxs/pm/user/userCfg/saveUser    ${data}    ${cookies}
    #检查创建结果3
    Check String    ${res}    true    contain
    #获取要删除的USER_ID们
    ${USER_ID1}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username3}'    USER_ID
    ${USER_ID2}    Get_Data_In_Mysql    ${mysqlInfo}    SELECT * FROM UPMS_USER where username='${username2}'    USER_ID
    #修改用户信息
    ${data}    Set variable    {"ids":"${USER_ID1},${USER_ID2}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/delUserList    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    删除选中用户成功    contain

上传用户
    ${res}    Http Upload    ${url}    /maxs/pm/user/userCfg/importTemplate    ${testFilePath}/平台管理/用户导入.xlsx    ${cookies}
    Check String    ${res}    "success":1    contain
    Check Count In Mysql    ${mysqlInfo}    select * from UPMS_USER where USERNAME ='test101'    1
    #删除
    ${id}    GET DATA IN MYSQL    ${mysqlInfo}    select USER_ID from UPMS_USER where USERNAME = 'test101'    USER_ID
    ${res}    HttpPost    ${url}    /maxs/pm/user/userCfg/delUser    {"userId":"${id}"}    ${cookies}
    #检查结果
    Check String    ${res}    删除用户成功    contain
    Check Count In Mysql    ${mysqlInfo}    select * from UPMS_USER where USERNAME ='test101'    0

