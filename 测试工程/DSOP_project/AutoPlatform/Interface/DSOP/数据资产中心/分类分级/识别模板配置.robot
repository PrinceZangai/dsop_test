*** Settings ***
Resource    ../../../Public/key.robot
Library    Collections

*** Variables ***
${addDataTagStrategy_url}    /dc-manager/api/dataTagStrategy/add
${deleteDataTagStrategy_url}    /dc-manager/api/dataTagStrategy/delete
${saveGrade_url}    /dc-manager/api/grade/save
${deleteGrade_url}    /dc-manager/api/grade/deleteGrade
${copyTemplate_url}    /dc-manager/api/classifyTemplate/copyClassifyTemplate
${deleteTemplate_url}    /dc-manager/api/classifyTemplate/deleteClassifyTemplate
${addClassification_url}    /dc-manager/api/classification/add
${deleteClassification_url}    /dc-manager/api/classification/delete?id=
${addRecognFeature_url}    /dc-manager/api/dataRecognFeature/save
${deleteRecognFeature_url}    /dc-manager/api/dataRecognFeature/delete?featureId=

*** Keywords ***
新增或更新分级
    [Arguments]    ${gradeName}    ${templateId}    ${color}
    [Documentation]    ${gradeName}分级名称    ${templateId}模板id    ${color}分级颜色
    ${request_json}    Create Dictionary    gradeName=${gradeName}    templateId=${templateId}    color=${color}
    ${resp}    请求    ${saveGrade_url}    POST    json=${request_json}
    [Return]    ${resp}

删除分级
    [Arguments]    ${id}
    [Documentation]    ${id}分级id
    ${resp}    请求    ${deleteGrade_url}    GET    params=id=${id}
    [Return]    ${resp}

新增标签识别策略
    [Arguments]    ${name}    ${templateId}    ${classificationId}    ${gradeId}    
    ...    ${featureNames}=${None}       ${featureIds}=${None}    ${isDesensitize}=0      
    [Documentation]    ${name}标签名称    ${templateId}模板id    ${classificationId}分类id    ${gradeId}分级id    
    ...    ${featureNames}特征名称       ${featureIds}特征id    ${isDesensitize}是否脱敏，0:否，1:是  
    ${request_json}    Create Dictionary    name=${name}    templateId=${templateId}    
    ...    classificationId=${classificationId}    gradeId=${gradeId}    featureNames=${featureNames}
    ...    featureIds=${featureIds}    isDesensitize=${isDesensitize}
    ${resp}    请求    ${addDataTagStrategy_url}    POST    json=${request_json}
    [Return]    ${resp}

删除标签识别策略
    [Arguments]    ${id}
    [Documentation]    ${id}标签id
    ${request_json}    Create Dictionary    id=${id}
    ${resp}    请求    ${deleteDataTagStrategy_url}    DELETE    json=${request_json}
    [Return]    ${resp}  

根据名称查询标签id
    [Arguments]    ${name}    ${template_id}
    [Documentation]    ${name}标签名称    ${template_id}模板id
    ${sql}    Set Variable    select id from td_data_tag_classification_strategy tdtcs where del_flag=0 and name='${name}' and template_id=${template_id};
    ${result}    Query    ${sql}
    [Return]    ${result}

根据名称查询分级id
    [Arguments]    ${name}    ${template_id}
    [Documentation]    ${name}标签名称    ${template_id}模板id
    ${sql}    Set Variable    select id,name from td_grade_dict tgd where del_flag=0 and name='${name}' and template_id=${template_id};
    ${result}    Query    ${sql}
    [Return]    ${result}

复制模板-空模板
    [Arguments]    ${templateId}=12    ${templateName}=复制空模版      ${isDefault}=0    ${remark}=初始化分级分类模板
    ${request_json}    Create Dictionary    templateId=${templateId}    templateName=${templateName}      isDefault=${isDefault}    remark=${remark}
    ${resp}    请求    ${copyTemplate_url}    POST    json=${request_json}
    [Return]    ${resp}

获取要删除复制模板的id
    ${sql}    Set Variable    select id from td_classify_template where name like '复制%'
    ${result}    Query    ${sql}
    [Return]    ${result}

删除复制模板-空模板
#根据id删除复制的模板
    ${result}    获取要删除复制模板的id
    ${request_json}    Create Dictionary    templateId=${result}[0][0]
    ${resp}    请求    ${deleteTemplate_url}    DELETE    json=${request_json}
    [Return]    ${resp}

新增分类
    [Arguments]    ${ancestors}=0    ${level}=0     ${templateId}=11     ${pid}=0     ${name}=123
    ${request_json}    Create Dictionary    ancestors=${ancestors}      level=${level}     templateId=${templateId}     pid=${pid}     name=${name}
    ${resp}    请求    ${addClassification_url}    POST    json=${request_json}
    [Return]    ${resp}

获取要删除分类的id
    [Arguments]    ${name}=22
    ${sql}    Set Variable     select id from td_classification_dict where name='${name}' order by id desc
    ${result}    Query    ${sql}
    [Return]     ${result}[0][0]

删除分类
    [Arguments]    ${id}=22864
    ${deleteClassification_url1}      Set Variable     ${deleteClassification_url}${id}
    ${resp}    请求    ${deleteClassification_url1}    DELETE
    [Return]    ${resp}

新增识别特征
    [Arguments]    ${name}=识别1     ${structType}=1     ${dataRecognFeatureRuleDtos}=[]     ${expect1}=1     ${dataRecognRuleRelationDtos1}=[]     ${combination1}=0
    ...    ${dataTagRuleDetailDtos1}=[]     ${type1}=1      ${matchType1}=5     ${ruleType1}=2     ${regex1}=11     ${enumContent1}=     ${expect2}=1
    ...    ${dataRecognRuleRelationDtos2}=[]     ${combination2}=0     ${dataTagRuleDetailDtos2}=[]     ${type2}=1      ${matchType2}=5     ${ruleType2}=2
    ...    ${regex2}=12     ${enumContent2}=
#    构造请求中的第一个字典，规则配置信息
    ${dataTagRuleDetailDtos1}     create list
    ${dataTagRuleDetailDtosDit1}    Create Dictionary    type=${type1}      matchType=${matchType1}     ruleType=${ruleType1}     regex=${regex1}       enumContent=${enumContent1}
    Append To List    ${dataTagRuleDetailDtos1}    ${dataTagRuleDetailDtosDit1}
    ${dataRecognRuleRelationDtos1}     create list
    ${dataRecognRuleRelationDtosDit1}     Create Dictionary     combination=${combination1}     dataTagRuleDetailDtos=${dataTagRuleDetailDtos1}
    Append To List     ${dataRecognRuleRelationDtos1}     ${dataRecognRuleRelationDtosDit1}
    ${dataRecognFeatureRuleDtosDit1}     Create Dictionary     expect=${expect1}     dataRecognRuleRelationDtos=${dataRecognRuleRelationDtos1}
#    构造请求中的第二个字典，例外规则配置信息
    ${dataTagRuleDetailDtos2}     create list
    ${dataTagRuleDetailDtosDit2}    Create Dictionary    type=${type2}      matchType=${matchType2}     ruleType=${ruleType2}     regex=${regex2}       enumContent=${enumContent2}
    Append To List    ${dataTagRuleDetailDtos2}    ${dataTagRuleDetailDtosDit2}
    ${dataRecognRuleRelationDtos2}     create list
    ${dataRecognRuleRelationDtosDit2}     Create Dictionary     combination=${combination2}     dataTagRuleDetailDtos=${dataTagRuleDetailDtos2}
    Append To List     ${dataRecognRuleRelationDtos2}     ${dataRecognRuleRelationDtosDit2}
    ${dataRecognFeatureRuleDtosDit2}     Create Dictionary     expect=${expect2}     dataRecognRuleRelationDtos=${dataRecognRuleRelationDtos2}
#    将上面两个字典放进列表中
    ${dataRecognFeatureRuleDtos}     create list
    Append To List    ${dataRecognFeatureRuleDtos}     ${dataRecognFeatureRuleDtosDit1}     ${dataRecognFeatureRuleDtosDit2}
#    整合整个请求（包括特征名称、数据类型），发送请求
    ${request_json}    Create Dictionary    name=${name}     structType=${structType}     dataRecognFeatureRuleDtos=${dataRecognFeatureRuleDtos}
    ${resp}    请求    ${addRecognFeature_url}    POST    json=${request_json}
    [Return]    ${resp}

获取要删除识别特征的id
    [Arguments]    ${name}=22
    ${sql}    Set Variable     select id from td_data_recognition_feature where name='${name}' order by id desc
    ${result}    Query    ${sql}
    [Return]     ${result}[0][0]

删除识别特征
    [Arguments]    ${id}=22864
    ${deleteRecognFeature_url1}      Set Variable     ${deleteRecognFeature_url}${id}
    ${resp}    请求    ${deleteRecognFeature_url1}    DELETE
    [Return]    ${resp}