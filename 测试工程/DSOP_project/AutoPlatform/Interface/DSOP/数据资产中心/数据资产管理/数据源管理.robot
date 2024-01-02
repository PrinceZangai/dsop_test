*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections

*** Variables ***
${interfacePath}    ../../../../../
${addDataResource_url}    /dc-manager/api/v1/dataResource/addDataResource    # 数据源添加
${deleteDataResource_url}    /dc-manager/api/v1/dataResource
${pageGetDataResource_url}    /dc-manager/api/v1/dataResource/list
${editResource_url}    /dc-manager/api/v1/dataResource/editResource
${detail_url}     /dc-manager/api/v1/dataResource/detail
${pageGetUnknownDataResource_url}    /dc-manager/api/v1/dataResource/unknown/page
${completeUnknownDataResource_url}    /dc-manager/api/v1/dataResource/addDataResource?unknownId=undefined


*** Keywords ***
新增数据源
    [Arguments]    ${name}    ${ipPortList}    ${userName}    ${password}    ${versionName}    ${serverPath}=    ${authMode}=${2}    ${businessId}=1    ${category}=2    ${isChangePwd}=True    ${type}=6    ${typeName}=MySQL    ${source}=4    ${status}=1    ${isCluster}=2    ${isOnline}=1
    ...    ${isScan}=2    ${optType}=create    ${owner}=admin    ${ownerName}=admin    ${businessName}=默认业务系统    @{attrModals}
    [Documentation]    ${attrModals} 其他配置信息 默认为空 格式为列表；
    ...    ${authMode} 认证方式 默认为2 密码认证；
    ...    |${businessId} 业务系统id dc默认为1；
    ...    ${category} 资源类别 默认为2 关系型数据库；
    ...    ${isChangePwd} 是否更改密码 默认为True；
    ...    ${serverPath}库名/文件路径
    ...    ${type} 资源类型字典值 默认为6 MySQL ；
    ...    ${typeName} 资源类型 默认为MySQL；
    ...    ${source} 资源来源 默认为4 备案；
    ...    ${status} 连接状态 默认为1 未连接；
    ...    ${isCluster} 是否集群 默认为2 否;
    ...    ${isOnline} 是否在线 默认为1 ;
    ...    |${isScan} 是否已梳理 默认为2；
    ...    ${optType} 数据源行为 默认为create 新增；
    ...    ${owner} 数据源责任人 默认为admin;
    ...    ${ownerName} 数据源责任人 默认为admin
    #业务系统信息    默认业务系统信息
    ${result}    根据业务系统名称获取业务系统信息    ${businessName}
    ${business}    Convert Keys To Camelcase    ${result}
    #数据源连接信息：用户名、密码、认证方式
    ${connectInfoMap}    create dictionary    authMode=${authMode}    serverPath=${serverPath}    userName=${userName}    password=${password}    isChangePwd=${True}
    #数据源节点信息dataResourceNodeModels    节点集合不能为空
    ${dataResourceNodeModels}    create list
    ${nodes_list}    create list
    FOR    ${node}    IN    @{ipPortList}
        ${dataResourceNodeModels_dict}    create dictionary    ip=${node}[ip]    port=${node}[port]    category=${category}    type=${type}    typeName=${typeName}    versionName=${versionName}    source=${source}    status=${status}
        ${nodes_dict}    create dictionary    ip=${node}[ip]    port=${node}[port]
        append to list    ${dataResourceNodeModels}    ${dataResourceNodeModels_dict}
        append to list    ${nodes_list}    ${nodes_dict}
    END
    ${nodes}    Evaluate    str(${nodes_list})
    ${nodes}    Replace String    ${nodes}    '    "
    ${IpPort_1}    create dictionary    ip=${ipPortList}[0][ip]    port=${ipPortList}[0][port]
    ${version}    Set Variable    2
    #目前还没有用到，先保留
    ${ip_port_1}    Set Variable
    ${kerberosAuthFiles}    Set Variable
    ${other_conn_0}    Set Variable
    #请求体
    ${json}    create dictionary    attrModals=@{attrModals}    authMode=${authMode}    businessId=${businessId}    category=${category}    connectInfoMap=${connectInfoMap}    connectStatus=${status}    dataResourceNodeModels=${dataResourceNodeModels}    ip_port_1=${ip_port_1}    IpPort_1=${IpPort_1}    isChangePwd=${isChangePwd}    isCluster=${isCluster}    isOnline=${isOnline}    isScan=${isScan}    kerberosAuthFiles=${kerberosAuthFiles}    name=${name}
    ...    nodes=${nodes}    optType=${optType}    other_conn_0=${other_conn_0}    owner=${owner}    ownerName=${ownerName}    serverPath=${serverPath}    source=${source}    type=${type}    typeName=${typeName}    version=${version}    versionName=${versionName}    business=${business}    isImportant=0
    ${resp}    请求    ${addDataResource_url}    POST    json=${json}
    [Return]    ${resp}

# 修改数据源
#     [Arguments]    ${id}    ${name}    ${isCluster}

删除数据源
    [Arguments]    ${name}
    [Documentation]    ${ids} 数据源id，列表
    ${resource_id}    根据数据源name获取数据源id    ${name}
    ${ids}    create list    ${resource_id}
    ${resp}    请求    ${deleteDataResource_url}    DELETE    json=${ids}
    [Return]    ${resp}

分页查询数据源
    [Arguments]    ${pageNo}=${1}    ${pageSize}=${10}    ${owners}=[]    ${deptIds}=[]    ${category}=[]    ${type}=[]
    [Documentation]    ${pageNo} 页号，默认为1
    ...    ${pageSize} 每页条数，默认为10
    ${request_json}    Create Dictionary    pageNo=${pageNo}    pageSize=${pageSize}    ${owners}=${owners}    ${deptIds}=${deptIds}    ${category}=${category}    ${type}=${type}
    ${resp}    请求    ${pageGetDataResource_url}    POST    json=${request_json}
#     ${dataResourceList}    Set Variable    ${resp}[data][list]
# #    Log To Console      ${dataResourceList}
#     #   获取列表的长度，初始为0，循环一次加1
#     ${length}    Set Variable      0
#     ${dataResourceList_ids}    Create List
#     FOR    ${element}    IN    @{dataResourceList}
#         ${length}    Evaluate    ${length} + 1
#         Append To List    ${dataResourceList_ids}    ${element}[id]     ${element}[name]     ${element}[nodes]     ${element}[isImportant]     ${element}[serverPath]     ${element}[isClusterDesc]     ${element}[isScanDesc]     ${element}[connectStatusDesc]
#     END
#     #   将列表的长度追加进结果列表
#     Append To List    ${dataResourceList_ids}    ${length}
#     Log To Console      ws+${dataResourceList_ids}
    [Return]    ${resp}

分页查询数据源-业务库查询
    ${sql}    Set Variable    select * from td_data_resource tdr order by create_time desc limit 0,10
    ${results}    Query    ${sql}
    Log To Console      ws2
    #   获取列表的长度，初始为0，循环一次加1
    ${length}=    Set Variable      0
    ${results_ids}    Create List
    FOR    ${element}    IN    @{results}
        ${length}=    Evaluate    ${length} + 1
#           转换是否集群字段值为字符串
        ${isImportant}=    Run Keyword If    ${element}[4] == 2    Set Variable    否
        ...    ELSE     Set Variable    是
#            转换是否梳理字段值为字符串
        ${isScan}=     Run Keyword If    ${element}[14] == 2    Set Variable    否
        ...    ELSE     Set Variable    是
#            转换连接状态字段值为字符串
        ${isConnet}=     Run Keyword If    ${element}[9] == 1    Set Variable   未连接
        ...    ELSE IF    ${element}[9] == 2    Set Variable   成功
        ...    ELSE     Set Variable    失败
        Append To List    ${results_ids}   ${element}[0]     ${element}[1]     ${element}[10]     ${element}[18]     ${element}[8]     ${isImportant}     ${isScan}     ${isConnet}
    END
    #   将列表的长度追加进结果列表
    Append To List    ${results_ids}    ${length}
    Log To Console      ws3+${results_ids}
    #返回该列表
    [Return]     ${results_ids}

查询数据源详情
    [Arguments]    ${name}
    [Documentation]    ${id} 数据源id
    ${id}    根据数据源name获取数据源id    ${name}
    ${url}    Set Variable    ${detail_url}/${id}
    ${resp}    请求    ${url}    GET
    should be equal as strings    操作成功    ${resp}[msg]
    ${data}    Get From Dictionary    ${resp}    data
    Get Dictionary Values    ${data}
    [Return]    ${data}

查询数据源详情-数据库
    [Arguments]    ${name}
    ${result}    根据数据源名称获取数据源信息    ${name}
    ${resource_info}    Convert Keys To Camelcase    ${result}

    [Return]    ${resource_info}

分页查询未知数据源
    [Arguments]     ${page}={}      ${pageNo}=1     ${pageSize}=10      ${dsPort}=    ${dsIp}=     ${dsTypeList}=[]

    #请求查询接口获得响应${resp}
    ${page}     Create Dictionary       pageNo=${pageNo}    pageSize=${pageSize}
    ${dsTypeList}       create list
    ${json}     Create Dictionary       page=${page}    dsPort=${dsPort}    dsIp=${dsIp}    pageNo=${pageNo}    dsTypeList=${dsTypeList}
    ${resp}    请求    ${pageGetUnknownDataResource_url}    POST       json=${json}

    #将查询到的未知数据源id、IP、端口、数据源类型、来源取出来放进一个列表中
    ${dataResourceList}    Set Variable    ${resp}[data][list]
    #   获取列表的长度，初始为0，循环一次加1
    ${length}=    Set Variable      0
    ${dataResourceList_result}    Create List
    FOR    ${element}    IN    @{dataResourceList}
        ${length}=    Evaluate    ${length} + 1
        Append To List    ${dataResourceList_result}    ${element}[id]      ${element}[dsIp]     ${element}[dsPort]     ${element}[dsType]      ${element}[source]
    END
    #   将列表的长度追加进结果列表
    Append To List    ${dataResourceList_result}    ${length}
#    Log To Console      ${dataResourceList_result}
    #返回该列表
    [Return]    ${dataResourceList_result}

分页查询未知数据源-业务库查询
     #业务库sql查询获得未知数据源表数据
    ${sql}    Set Variable    select * from td_unknown_datasource tdr order by create_time desc limit 0,10
    ${results}    Query    ${sql}

    #   获取列表的长度，初始为0，循环一次加1
    ${length}=    Set Variable      0
    #将sql查询到的未知数据源id、IP、端口、数据源类型、来源取出来放进一个列表中
    ${results_result}    Create List
    FOR    ${element}    IN    @{results}
        ${length}=    Evaluate    ${length} + 1
        ${port}     Convert To String      ${element}[2]
        Append To List    ${results_result}    ${element}[0]       ${element}[1]       ${port}       ${element}[3]       ${element}[7]
    END
    #   将列表的长度追加进结果列表
    Append To List    ${results_result}    ${length}
#    Log To Console      ${results_result}
    #返回该列表
    [Return]     ${results_result}

未知数据源补全-sftp
    [Arguments]     ${type}=9   ${serverPath}=/home     ${checkCluster}=false    ${ip_port_1}={}      ${ip}=10.21.171.142     ${port}=22     ${business}={}     ${id}=1
    ...     ${createBy}=admin      ${createTime}=2023-09-14 09:21:16    ${updateBy}=admin    ${updateTime}=2023-09-14 09:21:16    ${businessName}=默认业务系统     ${resPoolId}=1
    ...     ${deptList}=[]     ${deptId}=1     ${deptName}=全部    ${deptStr}=null      ${ipArea}=127.0.0.1     ${ports}=null     ${isDefault}=1     ${ownerId}=1
    ...    ${owner}=admin     ${labels}=null      ${delFlag}=0    ${IpPort_1}={}    ${dataResourceNodeModels}=[]
    ...    ${category}=1    ${typeName}=SFTP    ${source}=4    ${status}=2     ${isCluster}=2     ${connectInfoMap}={}     ${authMode}=2    ${userName}=aidm
    ...     ${password}=8uhb*UHB     ${isChangePwd}=true     ${attrModals}=[]      ${businessId}=1    ${name}=补全3    ${version}=     ${isOnline}=1    ${isScan}=2
    ...     ${source2}=6    ${connectStatus}=1     ${optType}=complete     ${isImportant}=0

    ${ip_port_1}     Create Dictionary     ip=${ip}     port=${port}
    ${deptDic}     Create Dictionary     deptId=${deptId}     deptName=${deptName}
    ${deptList}     Create List
    Append To List     ${deptList}     ${deptDic}
    ${business}     Create Dictionary     id=${id}    createBy=${createBy}      createTime=${createTime}    updateBy=${updateBy}    updateTime=${updateTime}    name=${businessName}     resPoolId=${resPoolId}    deptList=${deptList}
    ...    deptStr=${deptStr}      ipArea=${ipArea}     ports=${ports}     isDefault=${isDefault}     ownerId=${ownerId}    owner=${owner}     labels=${labels}      delFlag=${delFlag}
    ${IpPort_1}     Create Dictionary     ip=${ip}     port=${port}
    ${dataResourceNodeModels}     Create List
    ${dataResourceNodeModelsDic}     Create Dictionary    ip=${ip}     port=${port}     category=${category}    type=${type}    typeName=${typeName}    source=${source}    status=${status}
    Append To List     ${dataResourceNodeModels}     ${dataResourceNodeModelsDic}
    ${connectInfoMap}     Create Dictionary     authMode=${authMode}    serverPath=${serverPath}     userName=${userName}     password=${password}     isChangePwd=${isChangePwd}
    ${attrModals}     Create List
    ${nodes}    set variable    [{"ip":"${ip}","port":${port}}]
    ${json}    Create Dictionary     type=${type}    serverPath=${serverPath}     checkCluster=${checkCluster}    ip_port_1=${ip_port_1}     business=${business}     IpPort_1=${IpPort_1}
    ...    nodes=${nodes}    dataResourceNodeModels=${dataResourceNodeModels}     isCluster=${isCluster}    connectInfoMap=${connectInfoMap}     authMode=${authMode}            ${isChangePwd}=true
    ...    attrModals=${attrModals}      businessId=${businessId}    owner=${owner}    name=${name}    category=${category}     typeName=${typeName}     version=${version}     isOnline=${isOnline}    isScan=${isScan}     source=${source2}    connectStatus=${connectStatus}
    ...     optType=${optType}     isImportant=${isImportant}
    ${resp}    请求    ${completeUnknownDataResource_url}    POST       json=${json}
    [Return]    ${resp}

未知数据源补全-database
    [Arguments]     ${type}=7   ${serverPath}=prod     ${checkCluster}=false    ${ip_port_1}={}      ${ip}=10.21.171.142     ${port}=22     ${accessPermission}=admin
    ...    ${other_conn_1}={}     ${attrKey}=sys    ${attrValue}=sys1     ${IpPort_1}={}    ${dataResourceNodeModels}=[]
    ...    ${category}=2    ${typeName}=Oracle      ${versionName}=10g      ${source}=4     ${status}=2     ${isCluster}=2     ${connectInfoMap}={}     ${authMode}=2    ${userName}=aidm
    ...     ${password}=8uhb*UHB     ${isChangePwd}=true    ${attrModals}=[]    ${orclList}=[]    ${orcl}=prod    ${userName2}=sysdba     ${password}=sysdba     ${businessId}=1
    ...     ${owner}=admin    ${key}=1     ${isImportant}=1     ${name}=补全3    ${version}=3     ${isOnline}=1    ${isScan}=2     ${source2}=6    ${connectStatus}=1     ${optType}=complete

    ${ip_port_1}     Create Dictionary     ip=${ip}     port=${port}
    ${other_conn_1}     Create Dictionary     attrKey=${attrKey}    attrValue=${attrValue}
    ${IpPort_1}     Create Dictionary     ip=${ip}     port=${port}
    ${dataResourceNodeModels}     Create List
    ${dataResourceNodeModelsDic}     Create Dictionary    ip=${ip}     port=${port}     category=${category}    type=${type}    typeName=${typeName}    versionName=${versionName}    source=${source}    status=${status}
    Append To List     ${dataResourceNodeModels}     ${dataResourceNodeModelsDic}
    ${connectInfoMap}     Create Dictionary     authMode=${authMode}    serverPath=${serverPath}     userName=${userName}     password=${password}     isChangePwd=${isChangePwd}
    ${attrModals}     Create List
    ${attrModalsDic}     Create Dictionary     attrKey=${attrKey}    attrValue=${attrValue}
    Append To List     ${attrModals}    ${attrModalsDic}
    ${orclList}     Create List
    ${orclListDic}     Create Dictionary    orcl=${orcl}    userName=${userName2}     password=${password}     businessId=${businessId}     owner=${owner}    key=${key}    isImportant=${isImportant}
    Append To List     ${orclList}     ${orclListDic}
    ${nodes}    set variable    [{"ip":"${ip}","port":${port}}]
    ${json}    Create Dictionary     type=${type}   serverPath=${serverPath}     checkCluster=${checkCluster}    ip_port_1=${ip_port_1}     accessPermission=${accessPermission}     other_conn_1=${other_conn_1}
    ...     IpPort_1=${IpPort_1}    nodes=${nodes}      dataResourceNodeModels=${dataResourceNodeModels}     isCluster=${isCluster}     connectInfoMap=${connectInfoMap}     authMode=${authMode}
    ...     isChangePwd=${isChangePwd}    attrModals=${attrModals}      orclList=${orclList}     name=${name}    version=${version}     category=${category}    typeName=${typeName}      versionName=${versionName}
    ...      isOnline=${isOnline}    isScan=${isScan}     source=${source2}     connectStatus=${connectStatus}     optType=${optType}     owner=${owner}     isImportant=${isImportant}     businessId=${businessId}
    ...    password=${password}    userName=${userName2}

    ${resp}    请求    ${completeUnknownDataResource_url}    POST       json=${json}
    [Return]    ${resp}