*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections

*** Variables ***
${uploadToSampleFile_url}    /dc-manager/api/sampleFile/uploadToTempPath?scene={scene}&
${submitFileClusterTask_url}    /dc-manager/api/fileClusterTask/submit
${savefileModel_url}    /dc-manager/api/fileModel/save
${listTmpFiles_url}    /dc-manager/api/sampleFile/listTmpFiles
${batchDelFileClusterTask_url}    /dc-manager/api/fileClusterTask/batchDel
${deleteFileModel_url}    /dc-manager/api/fileModel/delete
${pageGetFileClusterTask_url}    /dc-manager/api/fileClusterTask/page
${pageGetFileModel_url}    /dc-manager/api/fileModel/page

*** Keywords ***
上传样本文件        
    [Arguments]    ${scene}    ${files}
    [Documentation]    ${scense}场景，聚类：cluster；分类：single    ${files}样本文件   
    ${url}    Replace String    ${uploadToSampleFile_url}    {scene}    ${scene}
    ${resp}    请求    ${url}    POST    files=${files} 
    [Return]    ${resp}

提交聚类任务
    [Arguments]    ${name}    ${filePath}    ${mlId}    ${thresholdValue}=80    ${id}=
    [Documentation]    ${name}任务名称    ${filePath}样本路径    
    ...    ${thresholdValue}相似度    ${mlId}机器学习模型id    ${id}
    ${request_json}    Create Dictionary    
    ...    name=${name}    filePath=${filePath}       thresholdValue=${thresholdValue}
    ...    mlId=${mlId}    id=${id}
    ${resp}    请求    ${submitFileClusterTask_url}    POST    json=${request_json}
    [Return]    ${resp}

分页查询聚类任务
    [Arguments]    ${pageNo}=1    ${pageSize}=10
    ${request_json}    Create Dictionary    pageNo=${pageNo}    pageSize=${pageSize}
    ${resp}    请求    ${pageGetFileClusterTask_url}    POST    json=${request_json}
    [Return]    ${resp}

分页查询分类任务
    [Arguments]    ${pageNo}=1    ${pageSize}=10
    ${request_json}    Create Dictionary    pageNo=${pageNo}    pageSize=${pageSize}
    ${resp}    请求    ${pageGetFileModel_url}    POST    json=${request_json}
    [Return]    ${resp}

删除聚类任务
    [Arguments]    ${ids}
    ${request_json}    Create Dictionary    ids=${ids}
    ${resp}    请求    ${batchDelFileClusterTask_url}    POST    json=${request_json}
    [Return]    ${resp}

删除分类任务
    [Arguments]    ${ids}
    ${request_json}    Create Dictionary    idList=${ids}
    ${resp}    请求    ${deleteFileModel_url}    POST    json=${request_json}
    [Return]    ${resp}

提交分类任务
    [Arguments]    ${name}    ${filePath}    ${mlId}    ${enableStopWords}=1    ${thresholdValue}=80    ${id}=    ${sampleFileList}=${None}
    [Documentation]    ${name}任务名称    ${filePath}样本路径    
    ...    ${thresholdValue}相似度    ${mlId}机器学习模型id    ${id}
    ${request_json}    Create Dictionary    
    ...    name=${name}    filePath=${filePath}       thresholdValue=${thresholdValue}
    ...    mlId=${mlId}    id=${id}    enableStopWords=${enableStopWords}    sampleFileList=${sampleFileList}
    ${resp}    请求    ${savefileModel_url}    POST    json=${request_json}
    [Return]    ${resp}

查询临时文件
    [Arguments]    ${filePath}
    ${url}    Set Variable    ${listTmpFiles_url}/${filePath}
    ${resp}    请求    ${url}    GET
    [Return]    ${resp}
