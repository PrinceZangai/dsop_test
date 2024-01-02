*** Variables ***
${host}           10.21.20.121
${hostname}       asap59
${ssh_username}    admin
${ssh_passwd}     BKYoMAEfpFb+YyTribgALVflEakgopWrizyzrp4yQsBgVSp04OkshuicaxcZD7EDn1iCp92yihj+jvm1YIaL6pf66F9H/5AXLYSfO2BFYMRnfejDvWtIi6B2RhjWE6LC3lPsW3FYSFCS7QxcCA==
${ssh_passwd_clear}    1qazXSW@6yhn
${ssh_port}       22
${url}            https://${host}:8686/    # http访问url，不含路径
${login_username}    admin
${login_passwd}    ZvEAqZT/dsymh0r5quvpsyiCwZSkI97tAgg+2m25zkvSWWW+WsDMAJP+oUSAnE+gjoLdLs9FA/LY/9+NG0lbz6GJHbfP+KRNlaCiZL21PkserjrvIZZEjnCtmcI/0AlEgKGCqgpkIsUQFfm2JdoYUCI4wB+mJN6GVUOm+V2zbFE=
${login_username1}    license@sys
${login_passwd1}    dN2Bh+TMyg3LoSkFAqsqqpzYZHSuaNN5yqtDg4LLU/vOST9JyGEgEzNjPFzrsACIa2Vd2xSUVnfidfsXCYpOT+bgWffMI1c5G7dy88TXuL/ksySsfMtzDFPNeJus5JJGmywiU9KUSgCr8jE/I91RUaAyyDzEGaaD68h3KKxz6NQ=
${login_username2}    sysadmin
${login_passwd2}    dN2Bh+TMyg3LoSkFAqsqqpzYZHSuaNN5yqtDg4LLU/vOST9JyGEgEzNjPFzrsACIa2Vd2xSUVnfidfsXCYpOT+bgWffMI1c5G7dy88TXuL/ksySsfMtzDFPNeJus5JJGmywiU9KUSgCr8jE/I91RUaAyyDzEGaaD68h3KKxz6NQ=
${login_username3}    maintainer@sys
${login_passwd3}    dN2Bh+TMyg3LoSkFAqsqqpzYZHSuaNN5yqtDg4LLU/vOST9JyGEgEzNjPFzrsACIa2Vd2xSUVnfidfsXCYpOT+bgWffMI1c5G7dy88TXuL/ksySsfMtzDFPNeJus5JJGmywiU9KUSgCr8jE/I91RUaAyyDzEGaaD68h3KKxz6NQ=
${mysqlInfo}      {"user":"root","password":"maxs.PDG~2022","host":"${host}","port":"3306","database":"SSA"}
${mysqlInfo1}     {"user":"root","password":"maxs.PDG~2022","host":"${host}","port":"3306","database":"SATP"}
${mysqlInfo2}     {"user":"root","password":"maxs.PDG~2022","host":"${host}","port":"6033","database":"SSA"}
${ckInfo}         {"user":"root","password":"maxs.PDG~2022","host":"${host}","port":"9002","database":"default"}
${proxyInfo}      {"user":"root","password":"maxs.PDG~2022","host":"${host}","port":"6033","database":"default"}
${zklInfo}        ${host}:2181
${esInfo}         {"protocol":"https","host":"${host}","port":"9200","http_auth":"elastic,maxs.PDG~2022"}
${mysqlHost}      ${host}
${kafkaHost}      ${host}
${redisHost}      192.168.112.201
${clusterMaster}  192.168.112.201
${MaxsPublicKey}    -----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChDnCJSDnLdKrK5QBv7hb+QNIWiC2slLOeWYUQhA7DKYKp7f6aKmWFE7mDRnA/LUoo26yxEJcfT9Wt2CzMmrjnRQDT3BmJxlWBHul90Hv1dMVdkrDn+dP7uXLLeiT4NFwbhLRMVYrMaXSdRDaRAG6g6oDIJfPM24XvBVZf3a/J7wIDAQAB\n-----END PUBLIC KEY-----


${DSOPUrl}        https://${web_ip}:8686
${alias}          DSOP
${LoginUrl}       /maxs/pm/sso/login/_login
${LogoutUrl}      /maxs/pm/sso/login/logout
${LoginUser}    zxj
${LoginPwd}    123456
${web_ip}         ${host}
@{MySQL配置}        ${web_ip}    3306    root    maxs.PDG~2022    DC
${DCPublicKey}    -----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkvEUyoCqPdpWuz8qGiI3waEYkc6IGMf44X9/RTs1lgl6OG1eJB2b+78fnRfvkhPC5Xt/6YnZDJ4KAiokmQgj+FW/Fw93DmDWkxcozUIFcOPhc1Oa93Bdze4yVObux+xMCgdTWNMbsicqXtTRkqVFYRIKMHTAjJfn33J+Lm5IWJwIDAQAB\n-----END PUBLIC KEY-----

${DC_db}    DC
${Maxs_DB}    SSA
