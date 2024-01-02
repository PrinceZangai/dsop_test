*** Settings ***
Resource    ../../../../../AutoPlatform/Interface/DSOP/数据资产中心/分类分级/识别模板配置.robot
Resource    ../../../../../AutoPlatform/Interface/Public/key.robot
Library    ../../../../../../../CustomKey/CommonLibrary/

*** Test Cases ***
新增标签识别策略
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P1
    ${name}    Set Variable    自动化测试-新增标签
    ${templateId}    Set Variable    12
    ${classificationId}    Set Variable    22726
    ${gradeId}    Set Variable    69
    ${resp}    新增标签识别策略    ${name}    ${templateId}    ${classificationId}    ${gradeId}
    Should Be Equal As Strings    新增数据标签策略成功    ${resp}[msg]

删除标签识别策略
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P1
    ${name}    Set Variable    自动化测试-新增标签
    ${templateId}    Set Variable    12
    ${result}    根据名称查询标签id    ${name}    ${templateId}
    ${resp}    删除标签识别策略    ${result}[0][0]
    Should Be Equal As Strings    删除数据标签策略成功    ${resp}[msg]

新增分级
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P1    @action=add
    ${gradeName}    Set Variable    自动化测试-新增分级
    ${templateId}    Set Variable    12
    ${color}    Set Variable    \#F4664A
    ${resp}    新增或更新分级    ${gradeName}    ${templateId}    ${color}
    Should Be Equal As Strings    新增或更新分级信息成功    ${resp}[msg]

删除分级
    [Tags]    @author=zeng.xj    @runlevel=smoke    @priority=P1
    ${gradeName}    Set Variable    自动化测试-新增分级
    ${templateId}    Set Variable    12
    ${result}    根据名称查询分级id    ${gradeName}    ${templateId}
    ${resp}    删除分级    ${result}[0][0]
    Should Be Equal As Strings    删除敏感等级成功    ${resp}[msg]

复制模板-删除模板
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P1
#    复制模板
    ${resp}    复制模板-空模板
    Should Be Equal As Strings    操作成功    ${resp}[msg]
#    删除复制出来的模板 待调试，环境有报错
    ${resp}    删除复制模板-空模板
    Should Be Equal As Strings    删除模板成功    ${resp}[msg]

新增分类-删除分类
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P1
    ${time}    get current timestamp
    ${name}    Set Variable    新增分类${time}
#    新增分类
    ${resp}    新增分类     name=${name}
    Should Be Equal As Strings    新增分类成功    ${resp}[msg]
#    删除分类
    ${result}    获取要删除分类的id    name=${name}
    ${resp}    删除分类     id=${result}
    Should Be Equal As Strings    删除分类成功    ${resp}[msg]

新增结构化识别特征-删除结构化识别特征
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P1
    ${time}    get current timestamp
    ${name}    Set Variable    新增识别特征${time}
#    新增识别特征
    ${resp}    新增识别特征     name=${name}      structType=1
    Should Be Equal As Strings    识别特征保存成功    ${resp}[msg]
#    删除识别特征
    ${result}    获取要删除识别特征的id    name=${name}
    ${resp}    删除识别特征     id=${result}
    Should Be Equal As Strings    操作成功    ${resp}[msg]

新增非结构化识别特征-删除非结构化识别特征
    [Tags]    @author=wang.shu    @runlevel=smoke    @priority=P1
    ${time}    get current timestamp
    ${name}    Set Variable    新增识别特征${time}
#    新增识别特征
    ${resp}    新增识别特征     name=${name}      structType=2
    Should Be Equal As Strings    识别特征保存成功    ${resp}[msg]
#    删除识别特征
    ${result}    获取要删除识别特征的id    name=${name}
    ${resp}    删除识别特征     id=${result}
    Should Be Equal As Strings    操作成功    ${resp}[msg]