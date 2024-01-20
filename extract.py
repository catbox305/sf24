import sqlalchemy as sq

test = sq.create_engine("sqlite+pysqlite:///data.db")
file = open("raw_data/top_excluding_sqlite.txt","a")

try:
    with test.connect() as db:
        result = db.execute(sq.text(
            """
            /*
            SELECT query, AVG(time)
            FROM data
            WHERE database='mysql' AND NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2')
            GROUP BY query
            ORDER BY query
            */
            SELECT query, database, MIN(time)
            FROM data
            WHERE NOT query IN ('short insert 1','short insert 2','long insert 1','long insert 2') AND NOT database='sqlite'
            GROUP BY query
            ORDER BY query
            """
        ))
        for row in result.fetchall():
            file.write(str(row[0].ljust(len("drop table if exists"))+" : "+row[1].ljust(len("postgresql"))+" : "+f"{row[2]:.12f}")+"\n")
finally:
    file.close()