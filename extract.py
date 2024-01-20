import sqlalchemy as sq

test = sq.create_engine("sqlite+pysqlite:///data.db")
file = [
    open("raw_data/mysql.txt","a"),
    open("raw_data/postgres.txt","a"),
    open("raw_data/sqlite.txt","a"),
    open("raw_data/top_no_sqlite.txt","a"),
    open("raw_data/top.txt","a")
    ]

try:
    with test.connect() as db:
        mysql = db.execute(sq.text(
            """SELECT query, AVG(time), database
            FROM data
            WHERE database='mysql' AND NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2')
            GROUP BY query
            ORDER BY query"""))
        pg = db.execute(sq.text(
            """SELECT query, AVG(time), database
            FROM data
            WHERE database='postgresql' AND NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2')
            GROUP BY query
            ORDER BY query"""))
        sqlite = db.execute(sq.text(
            """SELECT query, AVG(time), database
            FROM data
            WHERE database='sqlite' AND NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2')
            GROUP BY query
            ORDER BY query"""))
        
        top_no_sqlite = db.execute(sq.text(
            """SELECT query, MIN(time), database
            FROM data
            WHERE NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2') AND NOT database='sqlite'
            GROUP BY query
            ORDER BY query"""))
        top = db.execute(sq.text(
            """SELECT query, MIN(time), database
            FROM data
            WHERE NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2')
            GROUP BY query
            ORDER BY query"""))
        tmp = 0
        for i in [mysql,pg,sqlite,top_no_sqlite,top]:
            for row in i.fetchall():
                file[tmp].write(str(row[0].ljust(len("drop table if exists"))+" : "+row[1].ljust(len("postgresql"))+" : "+f"{row[2]:.12f}")+"\n")
            tmp+=1

finally:    
    for i in file:
     i.close()