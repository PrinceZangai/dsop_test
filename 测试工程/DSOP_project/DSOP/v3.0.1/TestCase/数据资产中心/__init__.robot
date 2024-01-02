*** Settings ***
Resource    ../../../../AutoPlatform/Interface/Public/key.robot
Suite Setup    Run Keywords    登录    连接DC_MySql
Suite Teardown    Run Keywords    登出    断开数据库