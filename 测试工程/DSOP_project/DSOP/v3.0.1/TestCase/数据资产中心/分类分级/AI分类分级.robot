*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/分类分级/AI分类分级.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/


*** Test Cases ***
新增聚类模型
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${filePath}    Set Variable    ${testFilePath}/分类分级/cluster
    ${files}    Create Files Data    directory=${filePath}
    ${resp}    上传样本文件    cluster    ${files}
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    
    ${finalFilePath}    Set Variable    ${resp}[data][finalFilePath]
    ${mlId}    Set Variable    ${resp}[data][mlId]
    ${resp}    提交聚类任务    自动化测试-聚类任务    ${finalFilePath}    ${mlId}
    Should Be Equal As Strings    操作成功    ${resp}[msg]  

删除聚类模型
    ${result}    根据名称获取id    自动化测试-聚类任务    ${DC_db}   td_ai_file_cluster_task    and del_flag=0
    ${ids}    Create List     ${{ ${result}[0][0] }}
    ${resp}    删除聚类任务    ${ids}
    Should Be Equal As Strings    操作成功    ${resp}[msg] 

新增分类模型
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${filePath}    Set Variable    ${testFilePath}/分类分级/single
    ${files}    Create Files Data    directory=${filePath}
    ${resp}    上传样本文件    single    ${files}
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    ${mlId}    Set Variable    ${resp}[data][mlId]
    ${finalFilePath}    Set Variable    ${resp}[data][finalFilePath]
    
    ${resp}    查询临时文件    single/${mlId}
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    
    ${data_from_resp}    Get Data From Datalist    ${resp}[data]    ${{ ['fileName','fileType','fileSize'] }}    ${True}
    ${resp}    提交分类任务    自动化测试-分类任务    ${finalFilePath}    ${mlId}    sampleFileList=${data_from_resp}
    Should Be Equal As Strings    操作成功    ${resp}[msg]

删除分类模型
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${model_name}    Set Variable    自动化测试-分类任务
    ${result}    Query    select id,name from td_ai_file_model where name='${model_name}' and del_flag=0;
    # 删除分类任务
    ${ids}    Create List     ${{ ${result}[0][0] }}
    ${resp}    删除分类任务    ${ids}
    Should Be Equal As Strings    操作成功    ${resp}[msg] 

分页查询分类任务
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
    ${resp}    分页查询分类任务
    Should Be Equal As Strings    操作成功    ${resp}[msg]
    # TODO 待校验具体字段

# 新增-删除聚类模型
#     [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
#     ${filePath}    Set Variable    project-AISDC/Conf/分类分级/cluster
#     ${files}    Create Files Data    directory=${filePath}
#     ${resp}    上传样本文件    cluster    ${files}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]
    
#     ${finalFilePath}    Set Variable    ${resp}[data][finalFilePath]
#     ${mlId}    Set Variable    ${resp}[data][mlId]
#     ${resp}    提交聚类任务    自动化测试-聚类任务    ${finalFilePath}    ${mlId}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]  

#     ${ids}    Create List     ${{ ${resp}[data][id] }}
#     ${resp}    删除聚类任务    ${ids}
#     Should Be Equal As Strings    操作成功    ${resp}[msg] 

# 新增-删除分类模型
#     [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P0
#     # 新增分类模型
#     ${filePath}    Set Variable    project-AISDC/Conf/分类分级/single
#     ${files}    Create Files Data    directory=${filePath}
#     ${resp}    上传样本文件    single    ${files}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]
#     ${mlId}    Set Variable    ${resp}[data][mlId]
#     ${finalFilePath}    Set Variable    ${resp}[data][finalFilePath]
#     # 查询模型文件列表
#     ${resp}    查询临时文件    single/${mlId}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]
#     # 保存分类任务
#     ${model_name}    Set Variable    自动化测试-分类任务
#     ${data_from_resp}    Get Data From Datalist    ${resp}[data]    ${{ ['fileName','fileType','fileSize'] }}    ${True}
#     ${resp}    提交分类任务    ${model_name}    ${finalFilePath}    ${mlId}    sampleFileList=${data_from_resp}
#     Should Be Equal As Strings    操作成功    ${resp}[msg]
#     # 分页查询分类任务
#     ${resp}    分页查询分类任务
#     Should Be Equal As Strings    操作成功    ${resp}[msg]

     
#     ${result}    执行sql    select id,name from td_ai_file_model where name='${model_name}' and del_flag=0;
#     # 删除分类任务
#     ${ids}    Create List     ${{ ${result}[0][0] }}
#     ${resp}    删除分类任务    ${ids}
#     Should Be Equal As Strings    操作成功    ${resp}[msg] 
    
# TODO 聚类应用为分类
# TODO 分类应用为模板标签
# TODO 修改分类模型
# TODO 修改聚类模型


