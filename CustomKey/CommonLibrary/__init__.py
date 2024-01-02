from CommonLibrary.GeneratorKeywords import Generator
from CommonLibrary.YamlKewrods import YamlUtil
from CommonLibrary.Common import Crypto,Requests
# from CommonLibrary.RedisKeyword import  RedisKeyword


class CommonLibrary(Generator,YamlUtil,Crypto,Requests,
                    # RedisKeyword,
                    ):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'