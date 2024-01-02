import random
import datetime
import pandas as pd
import os
import json

class Generator:
    """
            usage:
            *** Settings ***
                Library           RequestsLibrary
        |   *** Test Cases ***
        |   test_generator
                ${time}    get current timestamp
                log to console     ${time}
                ${date}    get current time
                log to console     ${date}
                ${random_string}    generate random alphanum    8
                log to console ${random_string}
        |
    """
    def get_current_time(self,format="%Y-%m-%d %H:%M:%S"):
        """
        | current_date
        | :param format: 字符串格式
        | :return: str
        """
        return datetime.datetime.now().strftime(format)

    def get_current_timestamp(self):
        """
        获取当前时间戳字符串
        :return: str
        """
        return int(datetime.datetime.now().timestamp()).__str__()


    def generate_random_alphanum(self,number=6,choices=None):
        """
        生成随机字符串
        :param number: 字符串长度
        :param choices: 自定义字符串选择范围，默认为大小写字母和数字
        :return:
        """
        if not choices:
            choices = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return "".join(random.choices(choices,k=number))

    def convert_keys_to_camelcase(self,dictionary):
        """
        将字典的键（key）从下划线式（snake_case）转换为驼峰式，且首字母小写
        :param dictionary: 需要转换的dict
        :return:dictionary

        original_dict = {"first_name": "John", "last_name": "Doe", "age": 30}
        converted_dict = convert_keys_to_camel_case(original_dict)
        print(converted_dict)
        {'firstName': 'John', 'lastName': 'Doe', 'age': 30}
        """
        converted_dict = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = self.convert_keys_to_camelcase(value)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            words = key.split('_')
            camel_case_key = ''.join([words[0].lower()] + [word.capitalize() for word in words[1:]])
            converted_dict[camel_case_key] = value
        return converted_dict

    def compare_dicts(self,dict1, dict2):
        """
        检查第一个字典的键是否也存在于第二个字典中，以及相应的值是否相等。如果找到任何不相等的值，函数将返回`False`，否则将返回`True`
        :param dict1:
        :param dict2:
        :return: False/True
        """
        for key in dict1.keys():
            if key in dict2.keys() and dict1[key] != dict2[key]:
                return False
        return True

    def get_data_from_datalist(self,dataList,columns=None,retainColumn=False):
        """_summary_
        |Exemples:
        |
        |    ${datalist} |   [{"name":"tom","age":12,"sex":"male"},{"name":"jerry","age":17,"sex":"male"}]
        |    ${data_from_datalist}   get data from datalist  | ${datalist} | columns=["name","sex"] 
        |    log to console | ${data_from_datalist} | [["tom","male"],["jerry","male"]] 
        |     
        |    ${sql_result} |   (("tom","age":12,"male"),("jerry","age":17,"male"))
        |    ${data_from_sql_result}   get data from datalist  | ${datalist} | columns=["0","2"] 
        |    log to console | ${data_from_sql_result} | [["tom","male"],["jerry","male"]] 

        Args:
        |    dataList (list like): 列表形式的数据（由接口返回或数据库查询得出）
        |    columns (list[str|int], optional): 需要提取的列，可以是列名或索引. Defaults to None.

        Returns:
        |    _type_: list like
        """
        result=[]
        if retainColumn:
            for item in dataList:
                result.append({col:item[col] for col in columns})
        else:
            for item in dataList:
                result.append([item[col] for col in columns])
        return result

    def get_data_from_excel(self,filename,sheet_name,columns=None):
        """_summary_

        Args:
        |    filename (str): 文件路径
        |    sheet_name (str): 表单名
        |    columns (list[str|int], optional): 需要提取的列，可以是列名或索引. Defaults to None.

        Returns:
        |    list: 返回二维列表
        """
        df = pd.read_excel(filename, sheet_name=sheet_name)
        if columns is None:
            return df.values.tolist()
        else:
            return df[columns].values.tolist()

    def get_data_from_csv(self,filename,columns=None):
        """_summary_

        Args:
            filename (str): 文件路径
            columns (list[str|int], optional): 需要提取的列，可以是列名或索引. Defaults to None.

        Returns:
            list: 返回二维列表
        """
        df = pd.read_csv(filename)
        if columns is None:
            return df.values.tolist()
        else:
            return df[columns].values.tolist()
    
    def create_files_data(self,*items,directory=None):
        list=[]
        if directory is not None:
            items=[os.path.join(directory,item) for item in os.listdir(directory)]
        for item in items:
            list.append(('files',open(item,'rb')))  # 此处关键字是files
        return list

    def convert_string_to_dictionary(self,string):
        return json.loads(string)     

if __name__ == '__main__':

    my_dict = {
        "first_name": "John",
        "last_name": "Doe",
        "date": datetime.datetime(2023, 9, 14, 9, 21, 16),
        "address_details": {
            "street_name": "123 Main St",
            "city_name": "New York"
        }
    }
    g = Generator()
    converted_dict = g.convert_keys_to_camelcase(my_dict)
    print(converted_dict)

