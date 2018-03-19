# coding=utf-8

import pymysql

db_host = 'localhost'
db_user = 'root'
db_pword = 'password'
db_name = 'zy_user'
db_charset = 'utf8'

#查询用户申请状态
def queryState(username,userID):
    jddb = pymysql.connect(host=db_host,
                           user=db_user,
                           passwd=db_pword,
                           db=db_name,
                           charset=db_charset)
    cursor = jddb.cursor()
    queryJdsql = "SELECT APPLY_STATE,FK_STATE,REMARK FROM USER_JDINFO WHERE APPUSER_NAME='%s' AND APPUSER_IDNO='%s'"%(username,userID)
    try:
        # 执行SQL语句,查询用户申请信息
        cursor.execute(queryJdsql)
        sqResults = cursor.fetchall()
        # 如果查询结果不为空，返回申请状态
        if sqResults:
            for row in sqResults:
                sq_state = row[0]
                fk_state = row[1]
                jd_remark = row[2]
        # 如果为空，返回提示信息
        else:
            sq_state = 'WARN'
    except pymysql.MySQLError:
        #print("Mysql Error %d: %s" % (pymysql.MySQLError.args[0], pymysql.MySQLError.args[1]))
        sq_state = 'WARN'
    # 关闭数据库连接
    jddb.close()
    return sq_state