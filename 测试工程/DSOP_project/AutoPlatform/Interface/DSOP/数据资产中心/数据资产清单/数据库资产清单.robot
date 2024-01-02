*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections


*** Variables ***
${exportDataAssetTables_url}    /dc-manager/api/dataAssetList/exportDataAssetTables
${exportDataAssetList_url}    /dc-manager/api/dataAssetList/export
${downloadFile_url}    /dc-manager/api/dataAssetList/downloadFilePath
${pageGetDataAssetTables_url}    /dc-manager/api/dataAssetList/page
${pageGetDataAssetList_url}    /dc-manager/api/dataAssetList/columnList


*** Keywords ***
数据资产表清单导出
    [Arguments]    ${templateId}    ${categoryIds}    ${resourceIds}=${None}    
    ...    ${resource}=${None}        
    ...    ${pageIndex}=1    ${tableName}=${None}    ${levelIds}=${None}
    ...    ${resourceCategorys}=${None}    ${resourceTypes}=${None}    
    ...    ${businessIds}=${None}    ${isAllDept}=1    ${isAllCategory}=1    
    ...    ${classifyIds}=${None}     ${listType}=table
    [Documentation]    
    ...    ${templateId}模板id    ${pageIndex}页码    ${pageSize}每页条数    ${tableName}表名
    ...    ${levelIds}分级id    ${resourceCategorys}数据源类别    ${resourceTypes}数据源类型
    ...    ${resource}数据源    ${pageNo}    ${businessIds}业务系统id    
    ...    ${isAllDept}是否所有部门    ${isAllCategory}是否所有类别    
    ...    ${classifyIds}分类id    ${categoryIds}数据源类别id

    ${request_json}    Create Dictionary    pageIndex=${pageIndex}    resourceIds=${resourceIds}    tableName=${tableName}
    ...    levelIds=${levelIds}    resourceCategorys=${resourceCategorys}    
    ...    resourceTypes=${resourceTypes}    resource=${resource}    
    ...    businessIds=${businessIds}    isAllDept=${isAllDept}    
    ...    isAllCategory=${isAllCategory}    templateId=${templateId}    
    ...    classifyIds=${classifyIds}    categoryIds=${categoryIds}    listType=${listType}
    ${resp}    请求-返回Response    ${exportDataAssetTables_url}    POST    json=${request_json}
    [Return]    ${resp}

数据资产字段清单导出
    [Arguments]    ${templateId}    ${pageIndex}=1    ${pageSize}=10        
    ...    ${pageNo}=1     ${tableName}=${None}    ${classifyIds}=${None}   
    ...    ${userIds}=${None}    ${deptIds}=${None}    ${resourceCategorys}=${None}    
    ...    ${resourceTypes}=${None}    ${isAllDept}=1    ${isAllCategory}=1    ${listType}="column"
    [Documentation]    
    ...    ${pageIndex} 当前页码    ${pageSize} 每页条数    ${pageNo}    
    ...    ${templateId} 当前默认模板id    ${tableName}     ${classifyIds} 分类id   
    ...    ${userIds} 用户id    ${deptIds} 部门id    ${resourceCategorys} 资源类型id    
    ...    ${resourceTypes}    ${isAllDept}    ${isAllCategory}    ${listType}

    ${request_json}    Create Dictionary      templateId=${templateId}    pageIndex=${pageIndex}    pageSize=${pageSize}        
    ...    pageNo=${pageNo}     tableName=${tableName}    classifyIds=${classifyIds}  
    ...    userIds=${userIds}    deptIds=${deptIds}   resourceCategorys=${resourceCategorys}   
    ...    resourceTypes=${resourceTypes}    isAllDept=${isAllDept}    isAllCategory=${isAllCategory}    listType=${listType}
    ${resp}    请求    ${exportdataAssetList_url}    POST    json=${request_json}
    [Return]    ${resp}

文件下载
    [Arguments]    ${filePath}    &{kwargs}
    [Documentation]    ${filePath} 文件路径

    ${params}    Create Dictionary    filePath=${filePath}
    ${request_json}    Create Dictionary
    FOR     ${key}    IN      @{kwargs}
        set to dictionary   ${request_json}   ${key}      ${kwargs}[${key}]
    END
    ${resp}    请求-返回Response    ${downloadFile_url}    POST    json=${request_json}    params=${params}    
    [Return]    ${resp}

分页查询数据资产表清单    
    [Arguments]    ${templateId}    ${categoryIds}    ${resourceIds}=[]
    ...    ${resource}=${None}        
    ...    ${pageIndex}=1    ${tableName}=${None}    ${levelIds}=${None}
    ...    ${resourceCategorys}=${None}    ${resourceTypes}=${None}    
    ...    ${businessIds}=${None}    ${isAllDept}=1    ${isAllCategory}=1    
    ...    ${classifyIds}=${None}     ${listType}=table    &{kwargs}
    [Documentation]    
    ...    ${pageIndex} 当前页码    ${pageSize} 每页条数    ${pageNo}    
    ...    ${templateId} 当前默认模板id    ${tableName}     ${classifyIds} 分类id   
    ...    ${userIds} 用户id    ${deptIds} 部门id    ${resourceCategorys} 资源类型id    
    ...    ${resourceTypes}    ${isAllDept}    ${isAllCategory}    ${listType}

    ${request_json}    Create Dictionary    pageIndex=${pageIndex}    tableName=${tableName}
    ...    levelIds=${levelIds}    resourceCategorys=${resourceCategorys}    resourceIds=${resourceIds}    
    ...    resourceTypes=${resourceTypes}    resource=${resource}    
    ...    businessIds=${businessIds}    isAllDept=${isAllDept}    
    ...    isAllCategory=${isAllCategory}    templateId=${templateId}    
    ...    classifyIds=${classifyIds}    categoryIds=${categoryIds}    listType=${listType}
    ${resp}    请求    ${pageGetDataAssetTables_url}    POST    json=${request_json}
    [Return]    ${resp}

分页查询数据资产字段清单
    [Arguments]    ${templateId}    ${resourceIds}=${None}    ${pageIndex}=1    ${pageSize}=10        
    ...    ${pageNo}=1     ${tableName}=${None}    ${classifyIds}=${None}   
    ...    ${userIds}=${None}    ${deptIds}=${None}    ${resourceCategorys}=${None}    
    ...    ${resourceTypes}=${None}    ${isAllDept}=1    ${isAllCategory}=1    ${listType}="column"
    [Documentation]    
    ...    ${pageIndex} 当前页码    ${pageSize} 每页条数    ${pageNo}    
    ...    ${templateId} 当前默认模板id    ${tableName}     ${classifyIds} 分类id   
    ...    ${userIds} 用户id    ${deptIds} 部门id    ${resourceCategorys} 资源类型id    
    ...    ${resourceTypes}    ${isAllDept}    ${isAllCategory}    ${listType}

    ${request_json}    Create Dictionary      templateId=${templateId}    resourceIds=${resourceIds}
    ...    pageIndex=${pageIndex}    pageSize=${pageSize}        
    ...    pageNo=${pageNo}     tableName=${tableName}    classifyIds=${classifyIds}  
    ...    userIds=${userIds}    deptIds=${deptIds}   resourceCategorys=${resourceCategorys}   
    ...    resourceTypes=${resourceTypes}    isAllDept=${isAllDept}    isAllCategory=${isAllCategory}    listType=${listType}
    ${resp}    请求    ${pageGetDataAssetList_url}    POST    json=${request_json}
    [Return]    ${resp}