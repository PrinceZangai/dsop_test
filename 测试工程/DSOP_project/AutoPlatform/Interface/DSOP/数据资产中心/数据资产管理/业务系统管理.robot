*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections

*** Variables ***
${addBusinessSys_url}    /dc-manager/api/businessSys/add
${deleteBatchBusinessSys_url}    /dc-manager/api/businessSys/deleteBatch
${pageGetBusinessSys_url}    /dc-manager/api/businessSys/page
${queryDeptUser_url}    /dc-manager/api/dataAssetList/queryDeptUser

*** Keywords ***
新增业务系统
    [Arguments]    ${name}    ${deptList}    ${ownerId}    ${owner}
    ...    ${ipArea}    ${ports}=${None}    ${labels}=${None}
    [Documentation]    ${name}业务系统名称    
    ...    ${deptList}部门列表，示例：[{deptId: "1", deptName: "全部"}]
    ...    ${ownerId}责任人id    ${ipArea}ip段    ${ports}端口    ${labels}标签    ${owner}责任人
    ${request_json}    Create Dictionary    name=${name}    deptList=${deptList}
    ...    ownerId=${ownerId}    ipArea=${ipArea}    ports=${ports}    
    ...    labels=${labels}    owner=${owner}
    ${resp}    请求    ${addBusinessSys_url}    POST    json=${request_json}
    [Return]    ${resp}

删除业务系统
    [Arguments]    ${ids}
    [Documentation]    ${ids}业务系统id
    ${request_json}    Create Dictionary    ids=${ids}
    ${resp}    请求    ${deleteBatchBusinessSys_url}    DELETE    json=${request_json}
    [Return]    ${resp}

分页查询业务系统
    [Arguments]    ${pageNo}=1    ${pageSize}=10
    ${request_json}    Create Dictionary    pageNo=${pageNo}    pageSize=${pageSize}
    ${resp}    请求    ${pageGetBusinessSys_url}    POST    json=${request_json}
    [Return]    ${resp}

查询组织用户
    [Arguments]    ${isEmptyDept}
    ${request_json}    Create Dictionary    isEmptyDept=${isEmptyDept}
    ${resp}    请求    ${queryDeptUser_url}    POST    json=${request_json}
    [Return]    ${resp}
