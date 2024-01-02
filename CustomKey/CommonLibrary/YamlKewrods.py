import yaml


class YamlUtil:
    """
    Yaml工具类，用于读取文件
    """
    def get_dictionary_from_file(self,file_path):
        """
        读取yaml文件，以字典形式返回
        :param file_path: 文件路径
        :return: dictionary
        """
        data = yaml.load(open(file_path, encoding="utf-8"), yaml.FullLoader)
        return data


    def get_value_from_file(self,file_path,key):
        if not key:
            return self.get_dictionary_from_file(file_path)
        else:
            return self.get_dictionary_from_file(file_path).get(key)

