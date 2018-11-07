import os
from subprocess import Popen, PIPE

def refreshDatabase():
    print("refreshDatabase...")
    databaseUri = 'postgresql://postgres:P$F$xs+n?5+Ug3AU5PTe3q@localhost/postgres'

    files = ['database_scripts/wipe_database.sql'
             , 'database_scripts/tables.sql'
             , 'database_scripts/data_codetables.sql'
             , 'database_scripts/test_data/TB_CONFIG.sql'
             , 'database_scripts/test_data/TB_USER_data.sql']
    for f in files:
        psqlCmd = ["psql", "-f", f, "-a", databaseUri]
        process = Popen(psqlCmd, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

if __name__ == "__main__":
    refreshDatabase()