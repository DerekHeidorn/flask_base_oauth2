import os
from subprocess import Popen, PIPE

def refreshDatabase():
    print("refreshDatabase...")
    databaseUri = 'postgresql://postgres:P$F$xs+n?5+Ug3AU5PTe3q@localhost/postgres'

    files = ['scripts/wipe_database.sql'
             , 'scripts/tables.sql'
             , 'scripts/data_codetables.sql'
             , 'scripts/test_data/TB_CONFIG.sql'
             , 'scripts/test_data/OAUTH.sql'
             , 'scripts/test_data/TB_USER_data.sql']
    for f in files:
        psqlCmd = ["psql", "-f", f, "-a", databaseUri]
        process = Popen(psqlCmd, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

if __name__ == "__main__":
    refreshDatabase()