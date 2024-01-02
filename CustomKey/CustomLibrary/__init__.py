from .ai.proxy import AiProxy
from .wakuangzhuanti.proxy import MineProxy
from .zhongbao.proxy import ProtectProxy
from .jiankong.proxy import MoniProxy
from .jiqunguanli.proxy import ClusterProxy
from .gaojing.proxy import AlarmProxy
from .xukeguanli.proxy import LicenseProxy
from .shujucaiji.proxy import CollectProxy
from .tongzhi.proxy import NotifyProxy
from .gongdan.proxy import OrderManageProxy
from .bi.proxy import BiProxy
# from .CkKEY import CkFunction
# from .EsKEY import EsFunction
from .HttpKEY import HttpFunction
from .KafkaKEY import KafkaFunction
from .MysqlKEY import MysqlFunction
from .SendUdpKEY import SendUdpFunction
from .SftpKEY import SftpFunction
from .SshKEY import SshFunction
from .StringKEY import StringFunction
from .TimeKEY import TimeFunction
from .WebsocketKEY import WsFunction
# from .ZkKEY import ZookeeperFunction
# from .captcha import CaptchaProxy
from .encrypt import Encryptor
# from .login import MaxsLogin

__verison__ = "1.0.0"


class CustomLibrary(HttpFunction,
                    TimeFunction,
                    MysqlFunction,
                    StringFunction,
                    # EsFunction,
                    # CkFunction,
                    # ZookeeperFunction,
                    SendUdpFunction,
                    SftpFunction,
                    SshFunction,
                    KafkaFunction,
                    WsFunction,
                    # CaptchaProxy,
                    Encryptor,
                    # MaxsLogin,
                    AiProxy,
                    MineProxy,
                    MoniProxy,
                    ClusterProxy,
                    ProtectProxy,
                    AlarmProxy,
                    LicenseProxy,
                    CollectProxy,
                    NotifyProxy,
                    OrderManageProxy,
                    BiProxy,
                    ):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
