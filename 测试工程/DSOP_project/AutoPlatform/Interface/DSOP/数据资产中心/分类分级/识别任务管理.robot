*** Settings ***
Resource    ../../../Public/key.robot
Library    DateTime
Library    Collections

*** Variables ***
${addScanTask_url}    /dc-manager/api/v1/data-recogn-job/create
${reconJobCompleteCheck_url}    /dc-manager/api/v1/data-recogn-job/{jobId}/complete/check
${getdataRecognJobById_url}    /dc-manager/api/v1/data-recogn-job
${listDataRecognJob_url}    /dc-manager/api/v1/data-recogn-job/list
${getStructAnalysisResult_url}    /dc-manager/api/v1/data-recogn-job/getStructAnalysisResult
${batchDelDataRecognJob_url}    /dc-manager/api/v1/data-recogn-job/batch-del

*** Keywords ***
获取数据源id
    [Arguments]    ${name}
    # \ \ \ 通过数据源名称获取数据源id，以备后续建扫描任务时需要
    ${sql}    set variable    select id from td_data_resource tdr where name ='${name}'
    log to console    ${sql}
    ${result}    query    ${sql}
    [Return]    ${result}[0][0]

获取识别模板id
    [Arguments]    ${name}
    # \ \ \ 通过识别模板名称获取数据源id，以备后续建扫描任务时需要
    ${sql}    set variable    select id from td_classify_template tdr where name ='${name}'
    log to console    ${sql}
    ${result}    query    ${sql}
    [Return]    ${result}[0][0]

新增扫描任务
    [Arguments]    ${name}=wss1   ${scanRange}=1    ${scope}=1    ${discoveryMode}=1    
    ...    ${jobType}=1    ${dsFreeTime}=00:00:00-23:59:59    
    ...    ${dataSourceRecognConfigDto}={}    ${planBeginTime}=    
    ...    ${planEndTime}=    ${cycleConfig}={}    ${templateList}=[]    
    ...    ${templateId}=24    ${commentBaseline}=60    ${fileRowSeparator}=\\n    
    ...    ${sampleMode}=2    ${sampleLine}=50    ${threadNum}=1
    ...    ${hitRate}=50    ${autoFeatureEnable}=2    ${isComment}=2    
    ...    ${rowCountEnable}=2    ${dsFreeTimeStr}=00:00:00-23:59:59    
    ...    ${dataSourceConnectInfoDtoList}=[]    ${cron}=    ${dateTime}=    
    ...    ${day}=[]    ${cycleType}=0    ${week}=[]    ${year}=[]    
    ...    ${dataSourceId}=35    ${id}=${dataSourceId}
    ${current_time}    Get Current Date    exclude_millis=True    
    ${planBeginTime}    Set Variable    ${current_time}
    ${planEndTime}    Add Time To Date    ${current_time}    7 days
    ${fileRowSeparator}    Set Variable    \n
    ${templateIdDic}    create dictionary    templateId=${templateId}
    ${templateList}    create list    ${templateIdDic}
    ${dataSourceDic}    create dictionary    dataSourceId=${dataSourceId}    id=${id}
    ${dataSourceConnectInfoDtoList}    create list    ${dataSourceDic}
    ${dataSourceRecognConfigDto}    create dictionary    discoveryMode=${discoveryMode}    scope=${scope}    scanRange=${scanRange}    templateList=${templateList}    commentBaseline=${commentBaseline}    fileRowSeparator=${fileRowSeparator}    sampleMode=${sampleMode}    sampleLine=${sampleLine}    threadNum=${threadNum}    hitRate=${hitRate}    autoFeatureEnable=${autoFeatureEnable}    isComment=${isComment}    rowCountEnable=${rowCountEnable}    dsFreeTimeStr=${dsFreeTimeStr}    jobType=${jobType}    dataSourceConnectInfoDtoList=${dataSourceConnectInfoDtoList}
    ${day}    create list
    ${week}    create list
    ${year}    create list
    ${cycleConfig}    create dictionary    cron=${cron}    dateTime=${dateTime}    day=${day}    cycleType=${cycleType}    week=${week}    year=${year}
    #Log To Console    ${cycleConfig}
    ${json}    create dictionary    name=${name}    scanRange=${scanRange}    scope=${scope}    discoveryMode=${discoveryMode}    jobType=${jobType}    dsFreeTime=${dsFreeTime}    dataSourceRecognConfigDto=${dataSourceRecognConfigDto}    planBeginTime=${planEndTime}    planEndTime=${planEndTime}    cycleConfig=${cycleConfig}
    ${resp}    请求    ${addScanTask_url}    POST    json=${json}
    [Return]    ${resp}

删除识别任务
    [Arguments]    @{ids}
    [Documentation]
    ${resp}    请求    ${batchDelDataRecognJob_url}    DELETE    json=${ids}
    [Return]    ${resp}

稽核
    [Arguments]    ${jobId}    ${templateIds}
    [Documentation]    ${jobId}任务id    ${templateId}模板id
    ${url}    Replace String    ${reconJobCompleteCheck_url}    {jobId}    ${jobId}
    ${params}    Create Dictionary    jobId=${jobId}    templateIds=${templateIds}
    ${resp}    请求    ${url}    PUT    params=${params}
    [Return]    ${resp}

查看识别任务详情
    [Arguments]    ${jobId}
    [Documentation]    ${jobId}任务id
    ${url}    set variable    ${getdataRecognJobById_url}/${jobId}
    ${resp}    请求    ${url}    GET
    [Return]    ${resp}

分页查询识别任务
    [Arguments]    ${pageNo}=1    ${pageSize}=10
    [Documentation]    ${pageNo}页码    ${pageSize}每条条数
    ${request_json}    Create Dictionary    pageNo=${pageNo}    pageSize=${pageSize}
    ${resp}    请求    ${listDataRecognJob_url}    POST    json=${request_json}
    [Return]    ${resp}

查询识别任务分析结果
    [Arguments]    ${jobId}    ${templateId}    ${dataType}=3    ${pageNo}=1    ${pageSize}=10
    [Documentation]    ${jobId}任务id    ${templateId}模板id
    ${request_json}    Create Dictionary    jobId=${jobId}    templateId=${templateId}    dataType=${dataType}    pageNo=${pageNo}    pageSize=${pageSize}
    ${resp}    请求    ${getStructAnalysisResult_url}    POST    json=${request_json}
    [Return]    ${resp}