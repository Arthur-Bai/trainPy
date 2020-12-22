#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import ibm_db,getpass


# In[ ]:


print("Please check db connections before run this script.\n", "*"*50 )
username = input("Database Username:")
password = getpass.getpass("Database Password:")


# In[ ]:


connstr = r'DATABASE=CSDW;HOSTNAME=trackeruat.rtp.dst.ibm.com;PORT=61030;PROTOCOL=TCPIP;UID=' + username + ';PWD=' + password + r';SECURITY=SSL;SSLCLIENTKEYSTOREDB=/Users/arthur/Documents/Work/DBA/DB2/ssl/mydbclient.kdb;SSLCLIENTKEYSTASH=/Users/arthur/Documents/Work/DBA/DB2/ssl/mydbclient.sth;'
conn = ibm_db.connect(connstr, "", "")


# In[ ]:


import re


# In[ ]:


# sql = "SELECT trim(tabschema) SOURCE_SCHEMA, trim(tabname) SOURCE_TABLE,  trim(tabschema) TARGET_SCHEMA, trim(tabname) TARGET_TABLE\
#     FROM syscat.tables \
#     WHERE TYPE = 'T'\
#     AND tabschema NOT LIKE 'SYS%'\
#     AND tabschema NOT LIKE 'DB2%' \
#     AND TABSCHEMA  NOT IN ('ASN','ASN_EXT','ASNPAN','ASN_MTH','CDC','UTOL','REPL','CLEVEILL') \
#     ORDER BY TABSCHEMA,TABNAME  \
#     fetch first 50 rows only "
# sql = "SELECT trim(tabschema) SOURCE_SCHEMA, trim(tabname) SOURCE_TABLE,  trim(tabschema) TARGET_SCHEMA, trim(tabname) TARGET_TABLE\
#         FROM syscat.tables \
#         WHERE TYPE = 'T'\
#         AND (tabschema LIKE 'CEDP%' \
#         or tabschema LIKE 'DSP%' \
#         or tabschema LIKE 'BRIOADMN%' \
#         or tabschema LIKE 'AUDIT%' )\
#             ORDER BY TABSCHEMA,TABNAME "
sql = "SELECT SOURCE_SERVER, TARGET_SERVER, m.SOURCE_OWNER SOURCE_SCHEMA, m.SOURCE_TABLE SOURCE_TABLE, m.TARGET_OWNER TARGET_SCHEMA, m.TARGET_TABLE TARGET_TABLE, m.PREDICATES FILTERS         FROM         ASN.IBMSNAP_SUBS_SET SET,         ASN.IBMSNAP_SUBS_MEMBR M         WHERE SET.apply_qual = M.apply_qual         AND SET.set_name = M.set_name         AND SOURCE_SERVER IN ('ODS', 'DSS', 'CSDW', 'WEB')"


# In[ ]:



stmt = ibm_db.exec_immediate(conn, sql)
# sourceDB = input('Please input sourceDB:')
# targetDB = input('Please input targetDB:')
env = input('Please input Env (VT/QA/PROD):')
mat = None
count = 1
## SQL statement contain at least 7 columns: SOURCE_DB, TARGET_DB, SOURCE_SCHEMA, SOURCE_TABLE, TARGET_SCHEMA, TARGET_TABLE, FILTERS
print("Connect to access and datastore","\n" , "#"*150)
print("connect server hostname %hostname% port %port% username %username% password %password%;")
print("connect datastore name %source% context source;")
print("connect datastore name %target% context target;")
while( ibm_db.fetch_row(stmt) ):
    
    sourceDB = ibm_db.result(stmt, "SOURCE_SERVER").strip()
    targetDB = ibm_db.result(stmt, "TARGET_SERVER").strip()
    s_schema = ibm_db.result(stmt, "SOURCE_SCHEMA").strip()
    s_table   = ibm_db.result(stmt, "SOURCE_TABLE").strip()
    t_schema = ibm_db.result(stmt, "TARGET_SCHEMA").strip()
    t_table   = ibm_db.result(stmt, "TARGET_TABLE").strip()
    filters   = ibm_db.result(stmt, "FILTERS")
    if (filters is not None):
        filters = filters.strip()
    subname = env + '_' + targetDB + '_' + sourceDB + '_' + t_schema.strip('0123456789')
    sourceid = env[:1] +  sourceDB[:1] + targetDB[:1] + '_' + t_schema.strip('0123456789')[:4]
    
    ## Group table mappings by target schema, even they are in different stage
    if ( mat is None or not re.match(t_schema.strip('0123456789'),mat)):
        count += 1
        mat = t_schema.strip('0123456789')
        print ( "\n\n"*2, "#"* 170,"\n"*2)
        print ( "# subscription for schema ", mat,"\n\n")
        print ( "add subscription name {} sourceid {};". format(subname.upper(), sourceid.upper()))
        print ( "select subscription name {};". format(subname.upper()))
        
        print ( "lock subscription name {};". format(subname.upper()))
    elif(mat is not None and re.match(t_schema.strip('0123456789'),mat)):
        # If next table schema is same as the previous one, generate table mapping directly
        pass

        
    print("add table mapping sourceSchema {0:<12} sourceTable {1:<42} targetSchema {2:<12}targetTable {3};".format(s_schema,s_table,t_schema,t_table), "# Table filters: ", filters)

## After all table mapped, disconnect access server
print("Total subscriptions:", count)
print("\n"*2,"#"* 170,"\ndisconnect server;")


# In[ ]:


# if ibm_db.active(conn):
#     sql = "SELECT DISTINCT TABSCHEMA \
#     FROM syscat.tables \
#     WHERE TYPE = 'T'\
#     AND tabschema NOT LIKE 'SYS%'\
#     AND tabschema NOT LIKE 'DB2%'\
#     AND TABSCHEMA  NOT IN ('ASN','ASN_EXT','ASNPAN','ASN_MTH','CDC','¬','REPL','CLEVEILL') WITH ur"
#     stmt = ibm_db.exec_immediate(conn, sql)
#     while( ibm_db.fetch_row(stmt) ):
#         name = ibm_db.result(stmt, "TABSCHEMA")
#         print("{}".format( name))
#         # print (result['TABNAME'])
# else:
#     print(ibm_db.conn_errormsg())


# In[ ]:


ibm_db.close(conn)

