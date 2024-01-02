# -*-coding: utf-8 -*-
import re


class StringFunction():
    def __init__(self):
        pass

    def check_string(self, srcvalue: str, checkvalue: str, expression: str):
        """

        断言方法，判断两个字符串是否相等包含等

        :param srcvalue: 必填，源字符串

        :param checkvalue: 必填，要校验的字符串

        :param expression: 必填，校验类型,有如下选项：equal,contain,startswith,endswith,regular

        举例：Check String    结果：操作成功    操作成功    contain
             表示检查字符串“结果：操作成功”中是否包含“操作成功”
        """
        if expression == 'equal':
            assert srcvalue == checkvalue, '源字符串：{}，不等于效验的值：{}'.format(srcvalue, checkvalue)
        elif expression == 'contain':
            assert checkvalue in srcvalue, '源字符串：{}，不包含：{}'.format(srcvalue, checkvalue)
        elif expression == 'startswith':
            assert srcvalue.startswith(checkvalue), '源字符串：{}，没有以字符串：{}开头'.format(srcvalue, checkvalue)
        elif expression == 'endswith':
            assert srcvalue.endswith(checkvalue), '源字符串：{}，没有以字符串：{}结尾'.format(srcvalue, checkvalue)
        elif expression == 'regular':
            assert re.search(r'{}'.format(checkvalue), srcvalue), '源字符串：{}，不能被此表达式：{}正则匹配'.format(srcvalue, checkvalue)
        else:
            raise RuntimeError('操作符：{}，不正确，请输入正确的操作符'.format(expression))

    def check_json(self, srcjson, keyname, expectvalue, expression: str):
        """
        断言方法，检查json里面的具体的key的值

        :param srcjson: 必填，源字符串

        :param keyname: 必填，要校验的KEY

        :param expectvalue: 必填，要校验的值

        :param expression: 必填，校验类型,有如下选项：equal,contain,startswith,endswith,regular

        举例：Check Json    {"message":"操作成功"}    message    操作成功    equal
             表示检查{"message":"操作成功"}中是否含有key：message，且他的值为：操作成功
        """
        srcjson_old = srcjson
        try:
            if not isinstance(srcjson, dict):
                # 前台传布尔值会是小写的true、false需转换
                srcjson = re.sub(':[ ]?true', ":True", srcjson)
                srcjson = re.sub(':[ ]?false', ":False", srcjson)
                srcjson = re.sub(':[ ]?null', ":None", srcjson)
                srcjson = eval(srcjson)
            assert isinstance(srcjson, dict)
        except Exception as e:
            raise RuntimeError('源字符串：{}是非json格式'.format(srcjson_old))
        if not isinstance(srcjson, dict): raise RuntimeError('源字符串：{}，是非json格式'.format(srcjson_old))
        if not (keyname in srcjson.keys()): raise RuntimeError('源字符串：{}，不包含此KEY：{}'.format(str(srcjson_old), keyname))
        if expression == 'equal':
            assert srcjson[keyname] == expectvalue, 'KEY:{}，在源数据中为：{}，和效验值：{}不相等'.format(keyname, srcjson[keyname],
                                                                                         expectvalue)
        elif expression == 'contain':
            if not isinstance(srcjson[keyname], str): raise RuntimeError(
                '效验的KEY：{}，值不是STRING，无法使用此方法'.format(srcjson[keyname]))
            if not isinstance(srcjson, str): raise RuntimeError('效验的值：{}，值不是STRING，无法使用此方法'.format(expectvalue))
            assert expectvalue in srcjson[keyname], 'KEY:{}，在源数据中为：{}，没有包含效验值：{}'.format(keyname, srcjson[keyname],
                                                                                         expectvalue)
        elif expression == 'startswith':
            if not isinstance(srcjson[keyname], str): raise RuntimeError(
                '效验的KEY：{}，值不是STRING，无法使用此方法'.format(srcjson[keyname]))
            if not isinstance(expectvalue, str): raise RuntimeError('效验的值：{}，值不是STRING，无法使用此方法'.format(expectvalue))
            assert srcjson[keyname].startswith(expectvalue), 'KEY:{}，在源数据中为：{}，不是以效验值：{}开头'.format(keyname,
                                                                                                   srcjson[keyname],
                                                                                                   expectvalue)
        elif expression == 'endswith':
            if not isinstance(srcjson[keyname], str): raise RuntimeError(
                '效验的KEY：{}，值不是STRING，无法使用此方法'.format(srcjson[keyname]))
            if not isinstance(expectvalue, str): raise RuntimeError('效验的值：{}，值不是STRING，无法使用此方法'.format(expectvalue))
            assert srcjson[keyname].endswith(expectvalue), 'KEY:{}，在源数据中为：{}，不是以效验值：{}结尾'.format(keyname,
                                                                                                 srcjson[keyname],
                                                                                                 expectvalue)
        elif expression == 'regular':
            if not isinstance(srcjson[keyname], str): raise RuntimeError(
                '效验的KEY：{}，值不是STRING，无法使用此方法'.format(srcjson[keyname]))
            if not isinstance(expectvalue, str): raise RuntimeError('效验的值：{}，值不是STRING，无法使用此方法'.format(expectvalue))
            assert re.search(r'{}'.format(expectvalue), srcjson[keyname]), 'KEY:{}，在源数据中为：{}，不能被此表达式：{}正则匹配'.format(
                keyname, srcjson[keyname],
                expectvalue)
        else:
            raise RuntimeError('操作符：{}不正确，请输入正确的操作符'.format(expression))

    def get_Split_String(self, srcvalue: str, separator, indexNo: int):
        """
        从string中提取字段方法

        :param srcvalue: 必填，源字符串

        :param separator: 必填，分隔符

        :param indexNo: 必填，要取的值的索引号，从1开始

        :return:返回处理后的字符串

        举例：Get Split String   'a:b:c'   :    3
            表示返回字符串：'a:b:c'以:切割的第3个值
        """
        list = srcvalue.split(separator)
        if int(indexNo) > len(list):
            raise RuntimeError('索引号越界，分隔后长度为{}'.format(str(len(list))))
        return srcvalue.split(separator)[int(indexNo) - 1]


if __name__ == '__main__':
    a = StringFunction()
    a.check_string('12aab', 'a', 'regular')
    json = "{'code': 200, 'message': '', 'data': [{'prop': 'TENANT_ID$name', 'label': '租户'}, {'prop': 'ORG_ID$name', 'label': '组织'}, {'prop': 'DEVICE_NAME', 'label': '设备名'}, {'prop': 'DOMAIN_ID$name', 'label': '安全域'}, {'prop': 'DEVICE_TYPE_ID$name', 'label': '设备类型'}, {'prop': 'DEVICE_MODEL', 'label': '设备型号'}, {'prop': 'CONFIRM_STATUS$name', 'label': '确认状态'}, {'prop': 'STATUS$name', 'label': '在线状态'}, {'prop': 'IS_KEY$name', 'label': '是否重要资产'}, {'prop': 'IS_AV_INSTALL$name', 'label': '是否安装防病毒'}, {'prop': 'BIZ_ID$name', 'label': '业务系统'}, {'prop': 'CREATE_TIME', 'label': '创建时间'}, {'prop': 'OS_ID$name', 'label': '操作系统类型'}, {'prop': 'UPDATE_TIME', 'label': '更新时间'}, {'prop': 'OS_VERSION', 'label': '操作系统版本'}, {'prop': 'GROUP_IDS$name', 'label': '资产组'}, {'prop': 'IS_EXPOSED$name', 'label': '是否暴露面资产'}, {'prop': 'IP_DETAILS.IP_NAME', 'label': 'IP名称'}, {'prop': 'IP_DETAILS.NETWORK_INTERFACE_CARD', 'label': 'IP网卡'}, {'prop': 'IP_DETAILS.IP', 'label': 'IP'}, {'prop': 'IP_DETAILS.MAC', 'label': 'MAC'}, {'prop': 'IP_DETAILS.SUBNET_MASK', 'label': '掩码'}, {'prop': 'IP_DETAILS.GATEWAY', 'label': '网关'}, {'prop': 'PORT_DETAILS.IP', 'label': 'IP'}, {'prop': 'PORT_DETAILS.PORT', 'label': '端口'}, {'prop': 'PORT_DETAILS.PROTOCOL', 'label': '端口协议'}, {'prop': 'PORT_DETAILS.SERVICE_NAME', 'label': '服务'}, {'prop': 'PORT_DETAILS.SERVICE_VERSION', 'label': '服务版本信息'}, {'prop': 'PORT_DETAILS.STATE', 'label': '状态'}, {'prop': 'SECURITY_DEPARTMENT_ID$name', 'label': '安全负责部门'}, {'prop': 'SECURITY_ADMIN$name', 'label': '安全负责人'}, {'prop': 'MAINTENANCE_DEPARTMENT_ID$name', 'label': '维护部门'}, {'prop': 'MAINTENANCE_ADMIN$name', 'label': '维护负责人'}, {'prop': 'CHARGER_ID$name', 'label': '合规负责人'}, {'prop': 'SERVER_MANAGE_IP', 'label': '服务器（HM）管理IP'}, {'prop': 'MAINTENANCE_ENDPOINT_IP', 'label': '维护终端IP'}, {'prop': 'CASCADE_SOURCE_NAME', 'label': '级联源平台'}, {'prop': 'CASCADE_SOURCE_IP', 'label': '级联源IP'}, {'prop': 'SOURCE$name', 'label': '创建来源'}, {'prop': 'CONNECTOIN_DETAILS.PROTOCOL$name', 'label': '协议'}, {'prop': 'CONNECTOIN_DETAILS.IP', 'label': 'IP'}, {'prop': 'CONNECTOIN_DETAILS.PORT', 'label': '端口'}, {'prop': 'CONNECTOIN_DETAILS.USERNAME', 'label': '用户名'}, {'prop': 'CONNECTOIN_DETAILS.PASSWORD', 'label': '密码'}, {'prop': 'CONNECTOIN_DETAILS.ENABLE_COMMAND', 'label': 'Enable口令'}, {'prop': 'CONNECTOIN_DETAILS.URL', 'label': 'URL'}, {'prop': 'CONNECTOIN_DETAILS.TNS_NAME', 'label': 'TNS名称'}, {'prop': 'CONNECTOIN_DETAILS.SERVICE_NAME', 'label': '服务名'}], 'ok': True}"
    a.check_json(json, 'message', '', 'equal')
    print(a.get_Split_String('a:b:c', ':', 3))
