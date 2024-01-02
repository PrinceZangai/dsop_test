*** Settings ***
# Suite Setup       GetCookies   ${url}  ${redisHost}  ${login_username}  ${login_passwd}
Suite Teardown    Run Keywords    Exec Sql In Mysql    ${mysqlInfo}    ${DelOrg}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${DelOrg2}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${DelOrgType}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${DelOrgType1}
...               AND    Exec Sql In Mysql    ${mysqlInfo}    ${DelOrgType2}
Resource          ../../../../../AutoPlatform/Interface/Public/KEY.robot
Resource          ../../../GlobalResource/config.robot

*** Variables ***
${OrgName}        二级组织1
${NewOrgName}     二级组织2
${OrgTypeName}    测试组织类型
${NewOrgTypeName}    新组织类型
${NewOrgTypeName2}    新组织类型2
${DelOrg}         DELETE from UPMS_ORGANIZATION where NAME='${OrgName}'
${DelOrg2}        DELETE from UPMS_ORGANIZATION where NAME='${NewOrgName}'
${DelOrg3}        DELETE from UPMS_ORGANIZATION where NAME='导入测试'
${DelOrgType}     DELETE from UPMS_ORG_TYPE where NAME='${OrgTypeName}'
${DelOrgType1}    update UPMS_ORG_TYPE set NAME='分支机构' where NAME='${NewOrgTypeName}'
${DelOrgType2}    DELETE from UPMS_ORG_TYPE where NAME='${NewOrgTypeName2}'

*** Test Cases ***
新增组织
    #创建组织请求
    ${data}    Set variable    {"name":"${OrgName}","pid":1,"orgType":1,"areaId":3,"outIp":"1.1.1.1","innerIpRange":"","description":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrganization    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    # ${SelectOrg}    Set variable    select * from UPMS_ORGANIZATION where NAME='${OrgName}'
    # ${checkdict}    Set variable    {"STATUS":"1","TENANT_ID":"-1"}
    # Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrg}    ${checkdict}

# 修改组织2
#     #获取OrgId
#     ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${OrgName}'    ORGANIZATION_ID
#     #修改Org信息
#     ${data}    Set variable    {"name":"${NewOrgName}","pid":-1,"orgType":1,"areaId":3,"outIp":"1.1.1.1","innerIpRange":"","description":"测试编辑组织","organizationId":${OrgId}}
#     ${res}    HttpPost    ${url}    /maxs/pm/user/org/updateOrganization    ${data}    ${cookies}
#     #检查结果
#     Check String    ${res}    true    contain
#     ${SelectOrg}    Set variable    select * from UPMS_ORGANIZATION where ORGANIZATION_ID='${OrgId}'
#     ${checkdict}    Set variable    {"STATUS":"1","TENANT_ID":"-1"}
#     Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrg}    ${checkdict}

编辑组织关联角色
    ${data}    Set variable    {"name":"${OrgName}","pid":1,"orgType":1,"areaId":3,"outIp":"1.1.1.1","innerIpRange":"","description":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrganization    ${data}    ${cookies}
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${OrgName}'    ORGANIZATION_ID
    #修改Org信息
    ${data}    Set variable    {"roleIds":"-1,1398569298327867394","organizationId":"${OrgId}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrUpdateOrganizationRole    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain

查询组织关联角色
    ${data}    Set variable    {"name":"${OrgName}","pid":1,"orgType":1,"areaId":3,"outIp":"1.1.1.1","innerIpRange":"","description":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrganization    ${data}    ${cookies}
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${OrgName}'    ORGANIZATION_ID
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/listOrganizationRole?organizationId=${OrgId}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

获取组织树
    ${data}    Set variable    {"name":"${OrgName}","pid":1,"orgType":1,"areaId":3,"outIp":"1.1.1.1","innerIpRange":"","description":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrganization    ${data}    ${cookies}
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${NewOrgName}'    ORGANIZATION_ID
    #修改Org信息
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/treeOrganization    ${EMPTY}    ${cookies}
    #检查结果
    Check String    ${res}    ${OrgId}    contain

获取页面列表
    #发送请求
    ${data}    Set variable    {"pageIndex":1,"pageSize":10,"orgTypeId":"","orgPathLike":""}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/pageOrganization    ${data}    ${cookies}
    #检查结果
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select count(*) as a from UPMS_ORGANIZATION where TENANT_ID=-1    a
    Check String    ${res}    ${OrgId}    contain

获取地区列表
    ${res}    HttpPost    ${url}    /maxs/pm/organization/getArea    ${EMPTY}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

获取子级地区(未知)
    ${res}    HttpGet    ${url}    maxs/pm/user/org/listArea?pid=0    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

根据组织Id获取负责人列表（业务不清楚）
    ${pid}    Set variable    1
    ${res}    HttpPost    ${url}    /maxs/pm/organization/getChildOrgUsersByOrgId    orgId=${pid}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain

获取全部子节点
    ${res}    HttpPost    ${url}    /maxs/pm/organization/getChildRenOrg    ${EMPTY}    ${cookies}
    #检查结果
    Check String    ${res}    200    contain
    #获取组织列表（分页）（报错了）
    #${res}    HttpPost    ${url}    /maxs/pm/organization/getOrganization    {}    ${cookies}
    #检查结果
    #Check String    ${res}    200    contain

getSelfAndChildren
    ${res}    HttpPost    ${url}    /maxs/pm/organization/getSelfAndChildren    ${EMPTY}    ${cookies}
    #检查结果
    Check String    ${res}    "code":200    contain
    #${cc}    Get Count    ${res}    "name":
    #${SelectOrgType}    Set variable    select count(*) as a from UPMS_ORGANIZATION where TENANT_ID=-1 and ORGANIZATION_ID =1 or PID=1
    #${checkdict}    Set variable    {"a":"${cc}"}
    #Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

获取角色
    #创建组织类型请求
    ${res}    HttpPost    ${url}    /maxs/pm/user/role/listRole    {}    ${cookies}
    #检查结果
    Check String    ${res}    "code":200    contain
    ${cc}    Get Count    ${res}    "roleId":
    ${SelectOrgType}    Set variable    select count(*) as a from UPMS_ROLE where TENANT_ID=-1
    ${checkdict}    Set variable    {"a":"${cc}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

删除组织前关联判断
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${NewOrgName}'    ORGANIZATION_ID
    #修改Org信息
    ${data}    Set variable    organizationId=${OrgId}
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/deleteCheckLink?${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain

删除组织前的子级判断
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${NewOrgName}'    ORGANIZATION_ID
    #修改Org信息
    ${data}    Set variable    organizationId=${OrgId}
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/deleteCheckSon?${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain

单个删除组织
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='${NewOrgName}'    ORGANIZATION_ID
    #删除Org
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/deleteOrganization?organizationId=${OrgId}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrg}    Set variable    select count(*) as a from UPMS_ORGANIZATION where ORGANIZATION_ID='${OrgId}'
    ${checkdict}    Set variable    {"a":"0"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrg}    ${checkdict}

获取组织类型
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/listOrganizationType    {}    ${cookies}
    #检查结果
    Check String    ${res}    "code":200    contain
    ${cc}    Get Count    ${res}    "name":
    ${SelectOrgType}    Set variable    select count(*) as a from UPMS_ORG_TYPE where TENANT_ID=-1
    ${checkdict}    Set variable    {"a":"${cc}"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

新增组织类型
    #创建组织类型请求
    ${data}    Set variable    {"name":"${OrgTypeName}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/saveOrganizationType    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrgType}    Set variable    select * from UPMS_ORG_TYPE where NAME='${OrgTypeName}'
    ${checkdict}    Set variable    {"IS_SYS":"0","TENANT_ID":"-1"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

修改内置组织类型
    #获取OrgTypeId
    ${OrgTypeId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORG_TYPE where IS_SYS='1' order by ID limit 1    ID
    #创建组织类型请求
    ${data}    Set variable    {"id":${OrgTypeId},"name":"${NewOrgTypeName}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/updateOrganizationType    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrgType}    Set variable    select * from UPMS_ORG_TYPE where NAME='${NewOrgTypeName}'
    ${checkdict}    Set variable    {"IS_SYS":"1","TENANT_ID":"-1"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

修改非内置组织类型
    #获取OrgTypeId
    ${OrgTypeId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORG_TYPE where NAME='${OrgTypeName}'    ID
    #创建组织类型请求
    ${data}    Set variable    {"id":${OrgTypeId},"name":"${NewOrgTypeName2}"}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/updateOrganizationType    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrgType}    Set variable    select * from UPMS_ORG_TYPE where NAME='${NewOrgTypeName2}'
    ${checkdict}    Set variable    {"IS_SYS":"0","TENANT_ID":"-1"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrgType}    ${checkdict}

删除非内置组织类型
    #获取OrgTypeId
    ${OrgTypeId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORG_TYPE where NAME='${NewOrgTypeName2}'    ID
    #删除组织类型请求
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/deleteOrganizationType?organizationTypeId=${OrgTypeId}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrgType}    Get_Data_In_Mysql    ${mysqlInfo}    select count(*) as a from UPMS_ORG_TYPE where NAME='${NewOrgTypeName2}'    a
    Check String    ${SelectOrgType}    0    contain

组织导入模板下载
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/downTemplate    ${cookies}
    #检查结果
    Check String    ${res}    P    contain

上传组织
    #修改默认组织内网网段信息
    ${data}    Set variable    {"name":"默认租户总部","pid":-1,"orgType":0,"areaId":1,"outIp":"","innerIpRange":"10.0.0.0-10.21.255.255,8.8.8.8","description":"管理组织","organizationId":1}
    ${res}    HttpPost    ${url}    /maxs/pm/user/org/updateOrganization    ${data}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    #上传二级组织
    ${res}    Http Upload    ${url}    /maxs/pm/user/org/importTemplate    ${CURDIR}\/..\/..\/..\/..\/GlobalResource\/TestFiles\/组织导入.xlsx    ${cookies}
    Check String    ${res}    "success":1    contain
    Check Count In Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='导入测试'    1
    #获取OrgId
    ${OrgId}    Get_Data_In_Mysql    ${mysqlInfo}    select * from UPMS_ORGANIZATION where NAME='导入测试'    ORGANIZATION_ID
    #删除Org
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/deleteOrganization?organizationId=${OrgId}    ${cookies}
    #检查结果
    Check String    ${res}    true    contain
    ${SelectOrg}    Set variable    select count(*) as a from UPMS_ORGANIZATION where ORGANIZATION_ID='${OrgId}'
    ${checkdict}    Set variable    {"a":"0"}
    Check Returnvalue In Mysql    ${mysqlInfo}    ${SelectOrg}    ${checkdict}

组织数据导出
    ${res}    HttpGet    ${url}    /maxs/pm/user/org/exportOrganization    ${cookies}
    #检查结果
    Check String    ${res}    P    contain
