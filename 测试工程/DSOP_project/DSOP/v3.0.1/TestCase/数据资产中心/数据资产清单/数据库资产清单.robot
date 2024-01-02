*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/数据资产清单/数据库资产清单.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/


*** Test Cases ***
数据资产表清单导出-全量
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${template_id}    Set Variable    11
    ${categoryIds}    Create List    2    3
    ${resp}    数据资产表清单导出    ${template_id}    ${categoryIds}
    ${timestamp}    Get Current Timestamp    
    ${fileName}    Set Variable    数据资产表清单_${timestamp}.xlsx
    ${data}    Set Variable    ${resp.content}
    Create Binary File    temp/${fileName}    ${data}
    # 连接数据库校验
    ${assertColumns}    Create List    表名    实例名    行数    识别模板    数据源    业务系统
    ${data_from_resp}     Get Data From Excel    temp/${fileName}    数据资产表清单    ${assertColumns}
    ${sql}    Set Variable     select assets_name,assets_path,if(tdati.rows=-1,"未统计",tdati.rows),tct.name,tdr.name,tbs.name from td_data_assets_table_inventory tdati join td_classify_template tct on tdati.template_id = tct.id join td_data_resource tdr on tdati.resource_id = tdr.id join td_business_sys tbs on tdr.business_id =tbs.id where template_id = ${template_id} and tdati.category in (2,3) order by tdati.id;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 6))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}
    Lists Should Be Equal    ${data_from_resp}    ${data_from_sqlresult}
    

数据资产字段清单导出-全量
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${template_id}    Set Variable    11
    ${resp}    数据资产字段清单导出    ${template_id}
    Should Be Equal As Strings    数据资产清单导出申请工单创建成功    ${resp}[msg]
    
    ${filePath}    Set Variable    ${resp}[data][filePath]
    ${None}    ${fileName}    Split Path    ${filePath}
    ${resp}    文件下载    ${filePath}
    ${data}    Set Variable    ${resp.content}
    Create Binary File    temp/${fileName}    ${data}
    # 连接数据库校验
    ${assertColumns}    Create List    数据源    实例名称    表名    业务系统
    ${data_from_resp}     Get Data From Csv    temp/${fileName}    ${assertColumns}
    ${sql}    Set Variable     select resource_name,DB_NAME,TABLE_NAME,biz_name from td_data_assets_lifecycle tdal where template_id =${template_id} and category in (2,3) and DATA_STATUS =0 order by id;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 4))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}
    Lists Should Be Equal    ${data_from_resp}    ${data_from_sqlresult}

分页查询数据资产表清单
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${template_id}    Set Variable    11
    ${categoryIds}    Create List    2    3
    ${resourceIds}    Create List    8
    ${resp}    分页查询数据资产表清单    ${template_id}    ${categoryIds}    resourceIds=${resourceIds}
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    # 校验资产名称、资产路径、行数、模板名称、资源名称、业务系统名称
    ${data}    Set Variable    ${resp}[data][data]
    ${assertColumns}    Create List    assetsName    assetsPath    rows    templateName    resourceName    businessName
    ${data_from_resp}     Get Data From Datalist       ${data}    ${assertColumns}
    ${sql}    Set Variable     select assets_name,assets_path,tdati.rows,tct.name,tdr.name,tbs.name from td_data_assets_table_inventory tdati join td_classify_template tct on tdati.template_id = tct.id join td_data_resource tdr on tdati.resource_id = tdr.id join td_business_sys tbs on tdr.business_id =tbs.id where template_id = ${template_id} and resource_id in (8) order by tdati.id;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 6))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}
    Lists Should Be Equal    ${data_from_resp}    ${data_from_sqlresult}
    
分页查询数据资产字段清单
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${template_id}    Set Variable    11
    ${resp}    分页查询数据资产字段清单    ${template_id}
    ${data}    Set Variable    ${resp}[data][data]
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    ${assertColumns}    Create List    resourceName    dbName    tableName    businessName
    ${data_from_resp}     Get Data From Datalist    ${data}    ${assertColumns}
    ${sql}    Set Variable     select resource_name,DB_NAME,TABLE_NAME,biz_name from td_data_assets_lifecycle tdal where template_id =${template_id} and category in (2,3) and DATA_STATUS =0 order by id limit 0,10;
    ${results}    Query    ${sql}
    ${assertIndices}    Evaluate    list(range(0, 4))
    ${data_from_sqlresult}    Get Data From Datalist    ${results}    ${assertIndices}
    Lists Should Be Equal    ${data_from_resp}    ${data_from_sqlresult}