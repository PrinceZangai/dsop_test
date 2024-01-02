*** Settings ***
Resource          ../../../../../AutoPlatform/Interface/Public/key.robot
Resource          ../../../GlobalResource/config.robot
# Suite Setup       GetCookies    ${url}    ${redisHost}    ${login_username}    ${login_passwd}


*** Variables ***

*** Test Cases ***
获取所有设备
    ${res}    Http Post    ${url}    /data-access/quickCreate/getAllCreate    ${EMPTY}    ${cookies}    30
    # Check String    ${res}    "DEVICE_TYPE":"ASIA_TDA"    contain

获取所有接口
    ${res}    Http Post    ${url}    /data-access/quickCreate/getAllPort    ${EMPTY}    ${cookies}    30
    Check String    ${res}    8805    contain

获取设备详情
    #新增设备
    ${random1}    Evaluate    random.randint(0,10000)    random
    ${port}    Evaluate    random.randint(0,10000)    random
    ${DEVICE_NAME}    Catenate    SEPARATOR=    device__    ${random1}
    ${data}    Set variable    {"COMPANY_NAME":"亚信安全","DEVICE_IP":"10.21.47.117","DEVICE_NAME":"${DEVICE_NAME}","DEVICE_SN":"DDDDD","DEVICE_TYPE":"${DEVICE_NAME}","DEVICE_VERSION":"8.2","ICON_PATH":"icon-wangluoxitong","PORT_DEFAULT":${port},"REMARK":"","RULE_ID":6}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/addAccessDevice    ${data}    ${cookies}    30    #新增设备
    check String    ${res}    success    contain
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from AUS_COLLECT_ONEKEY_CREATE where DEVICE_NAME='${DEVICE_NAME}'    ID
    ${data}    Set Variable    {"id":${id}}
    ${res}    Http Post    ${url}    /data-access/quickCreate/getUdpConfig    ${data}    ${cookies}    30
    Check String    ${res}    "DEVICE_NAME":"${DEVICE_NAME}"    contain

新增设备
    ${random1}    Evaluate    random.randint(0,10000)    random
    ${port}    Evaluate    random.randint(0,10000)    random
    ${DEVICE_NAME}    Catenate    SEPARATOR=    device__    ${random1}
    ${data}    Set variable    {"COMPANY_NAME":"亚信安全","DEVICE_IP":"10.21.47.117","DEVICE_NAME":"${DEVICE_NAME}","DEVICE_SN":"DDDDD","DEVICE_TYPE":"${DEVICE_NAME}","DEVICE_VERSION":"8.2","ICON_PATH":"icon-wangluoxitong","PORT_DEFAULT":${port},"REMARK":"","RULE_ID":6}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/addAccessDevice    ${data}    ${cookies}    30    #新增设备
    check String    ${res}    success    contain

修改设备
    ${random1}    Evaluate    random.randint(0,10000)    random
    ${port}    Evaluate    random.randint(0,10000)    random
    ${DEVICE_NAME}    Catenate    SEPARATOR=    device__    ${random1}
    ${random2}    Evaluate    random.randint(0,10000)    random
    ${new_DEVICE_NAME}    Catenate    SEPARATOR=    device__    ${random2}
    ${port1}    Evaluate    random.randint(0,10000)    random
    ${data}    Set variable    {"COMPANY_NAME":"亚信安全","DEVICE_IP":"10.21.47.117","DEVICE_NAME":"${DEVICE_NAME}","DEVICE_SN":"DDDDD","DEVICE_TYPE":"${DEVICE_NAME}","DEVICE_VERSION":"8.2","ICON_PATH":"icon-wangluoxitong","PORT_DEFAULT":${port},"REMARK":"","RULE_ID":6}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/addAccessDevice    ${data}    ${cookies}    30    #新增设备
    check String    ${res}    success    contain
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from AUS_COLLECT_ONEKEY_CREATE where DEVICE_NAME='${DEVICE_NAME}'    ID
    ${data}    Set variable    {"COMPANY_NAME":"亚信安全","DEVICE_IP":"10.21.47.117","DEVICE_NAME":"${new_DEVICE_NAME}","DEVICE_SN":"DDDDD","DEVICE_TYPE":"${DEVICE_NAME}","DEVICE_VERSION":"8.2","ICON_PATH":"icon-wangluoxitong","ID":"${id}","PORT_DEFAULT":${port1},"REMARK":"","RULE_ID":6}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/updateAccessDevice    ${data}    ${cookies}    30
    check String    ${res}    success    contain

删除设备
    ${random1}    Evaluate    random.randint(0,10000)    random
    ${port}    Evaluate    random.randint(0,10000)    random
    ${DEVICE_NAME}    Catenate    SEPARATOR=    device__    ${random1}
    ${data}    Set variable    {"COMPANY_NAME":"亚信安全","DEVICE_IP":"10.21.47.117","DEVICE_NAME":"${DEVICE_NAME}","DEVICE_SN":"DDDDD","DEVICE_TYPE":"${DEVICE_NAME}","DEVICE_VERSION":"8.2","ICON_PATH":"icon-wangluoxitong","PORT_DEFAULT":${port},"REMARK":"","RULE_ID":6}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/addAccessDevice    ${data}    ${cookies}    30    #新增设备
    check String    ${res}    success    contain
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from AUS_COLLECT_ONEKEY_CREATE where DEVICE_NAME='${DEVICE_NAME}'    ID
    ${data}    Set Variable    {"ID":${id}}
    ${res}    HttpPost    ${url}    /data-access/quickCreate/deleteAccessDevice    ${data}    ${cookies}    30    #删除设备
    check String    ${res}    success    contain

一键接入创建dp-ESM
    ${random1}    Get Date    days    0    %Y%m%d%H%M%S%f
    ${topic}    Set variable    MAXS_COLLECT_${random1}
    ${random2}    Evaluate    random.randint(0,10000)    random
    ${flume_name}    Catenate    SEPARATOR=    esm_    ${random2}
    ${port}    Evaluate    random.randint(0,10000)    random
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from AUS_COLLECT_ONEKEY_CREATE where DEVICE_TYPE='ASIA_ESM'    ID
    ${data}    Set variable    {"config":{"host":52,"port":${port},"deviceId":${id}},"name":"${flume_name}","partition":1,"remark":"","replica":1,"topic":"${topic}","type":0}
    ${res}    HttpPost    ${url}    /data-access/flume/create    ${data}    ${cookies}    30
    check String    ${res}    保存成功    contain
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_SPIDER where NAME='${flume_name} '    ID
    ${data}    Set variable    {"name":"${flume_name}","ruleId":6,"spiderId":${id},"desc":""}
    ${res}    HttpPost    ${url}    /data-access/process/pipeline/createTaskByOneKeyCreate    ${data}    ${cookies}    30
    check String    ${res}    创建成功    contain
    #删除dp
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_PIPELINE_INSTANCE where NAME='${flume_name} '    ID
    ${data}    Set variable    {"id":${id}}
    ${res}    HttpPost    ${url}    /data-access/process/pipeline/deleteTask    ${data}    ${cookies}    30
    check String    ${res}    删除成功    contain
    #删除flume
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_SPIDER where NAME='${flume_name} '    ID
    ${data}    Set variable    {"id":${id}}
    ${res}    HttpPost    ${url}    /data-access/flume/delete    ${data}    ${cookies}    30
    check String    ${res}    删除成功    contain

一键接入创建dp-TDA
    ${random1}    Get Date    days    0    %Y%m%d%H%M%S%f
    ${topic}    Set variable    MAXS_COLLECT_${random1}
    ${random2}    Evaluate    random.randint(0,10000)    random
    ${flume_name}    Catenate    SEPARATOR=    tda_    ${random2}
    ${port}    Evaluate    random.randint(0,10000)    random
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from AUS_COLLECT_ONEKEY_CREATE where DEVICE_TYPE='ASIA_TDA'    ID
    ${data}    Set variable    {"config":{"host":52,"port":${port},"deviceId":${id}},"name":"${flume_name}","partition":1,"remark":"","replica":1,"topic":"${topic}","type":0}
    ${res}    HttpPost    ${url}    /data-access/flume/create    ${data}    ${cookies}    30
    check String    ${res}    保存成功    contain
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_SPIDER where NAME='${flume_name}'    ID
    ${data}    Set variable    {"name":"${flume_name}","ruleId":1,"spiderId":${id},"desc":""}
    ${res}    HttpPost    ${url}    /data-access/process/pipeline/createTaskByOneKeyCreate    ${data}    ${cookies}    30
    check String    ${res}    创建成功    contain
    #删除dp
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_PIPELINE_INSTANCE where NAME='${flume_name}'    ID
    ${data}    Set variable    {"id":${id}}
    ${res}    HttpPost    ${url}    /data-access/process/pipeline/deleteTask    ${data}    ${cookies}    30
    check String    ${res}    删除成功    contain
    #删除flume
    ${id}    Get Data In Mysql    ${mysqlInfo}    select ID from PREPROCESS_SPIDER where NAME='${flume_name}'    ID
    ${data}    Set variable    {"id":${id}}
    ${res}    HttpPost    ${url}    /data-access/flume/delete    ${data}    ${cookies}    30
    check String    ${res}    删除成功    contain
