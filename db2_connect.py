import ibm_db,getpass

# password = getpass.getpass("Password:")
password = ''

connstr = r'DATABASE=ODS;HOSTNAME=commander.rtp.dst.ibm.com;PORT=61010;PROTOCOL=TCPIP;UID=baiyx;PWD=' + password + r';SECURITY=SSL;SSLCLIENTKEYSTOREDB=C:\Work\DBA\DB2\SSL\kdb\mydbclient.kdb;SSLCLIENTKEYSTASH=C:\Work\DBA\DB2\SSL\kdb\mydbclient.sth;'
conn = ibm_db.connect(connstr, "", "")
if conn:
    sql = "SELECT * from syscat.tables fetch first 10 rows only with ur"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_both(stmt)
    while( result ):
        print ("Result :", result['TABSCHEMA'])
        # print (result['TABNAME'])
        result = ibm_db.fetch_both(stmt)
