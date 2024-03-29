import sys
import time
import asyncio
import sqlalchemy as sq
import random

open("sqlite3.db","w").close()
open("data.db","w").close()

raise Exception("\n\nTest failed, remove line 10 of raw.py and try again.\n\n") # Remove this line

sqlite = sq.create_engine("sqlite+pysqlite:///sqlite3.db")
postgres = sq.create_engine("postgresql+pg8000://USER:PASSWORD@localhost:PORT/DB") # Fill in placeholders before running
mysql = sq.create_engine("mysql+pymysql://USER:PASSWORD@localhost/DB") # FIll in placeholders before running
log = sq.create_engine("sqlite+pysqlite:///data.db")

with log.connect() as con:
    con.execute(sq.text("CREATE TABLE IF NOT EXISTS data (time float(11), query varchar(100), database varchar(100))"))

def test(engine,eta,log=log):
    
    print(f"[Test {eta}/30] Estimated time remaining: {(527-(eta*17))}s")

    strings = ["".join(random.choices("q w e r t y u i o p a s d f g h j k l z x c v b n m".split(),k=20)) for i in range(100000)]
    numbers = [random.randint(1000,9000) for i in range(100000)]
    both = [strings,numbers]
    #data = [(both[0][i], both[1][i]) for i in range(len(both[0]))]
    data1 = [{"token":both[0][i]} for i in range(len(both[0]))]
    data2 = [{"id":both[1][i]} for i in range(len(both[1]))]
    data3 = [{"token":both[0][i], "id":both[1][i]} for i in range(len(both[0]))]


    with engine.connect() as db:
        db.info.setdefault("dbname", []).append(engine.name)

        @sq.event.listens_for(db, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):

            conn.info.setdefault("query_start_time", []).append(time.time())


        @sq.event.listens_for(db, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany, testdata=log):

            total = time.time() - conn.info["query_start_time"].pop(-1)

            with testdata.connect() as db:

                db.execute(sq.text("INSERT INTO data (time, query, database) VALUES (:time, :query, :database)"),{"time":total, "query":str(statement.split("*")[1].strip()), "database":conn.info["dbname"][0]})


        
        db.execute(sq.text("/* drop table if exists */ DROP TABLE IF EXISTS test"))

        db.execute(sq.text("/* create table */ CREATE TABLE test (token varchar(100), id int)"))

        db.execute(sq.text("/* short insert 1 */ INSERT INTO test (token) VALUES (:token)"), data1[0:101])

        db.execute(sq.text("/* short insert 2 */ INSERT INTO test (id) VALUES (:id)"), data2[0:101])

        db.execute(sq.text("/* short insert */ INSERT INTO test (token, id) VALUES (:token, :id)"), data3[0:101])

        db.execute(sq.text("/* long insert 1 */ INSERT INTO test (token) VALUES (:token)"), data1)

        db.execute(sq.text("/* long insert 2 */ INSERT INTO test (id) VALUES (:id)"), data2)

        db.execute(sq.text("/* long insert */ INSERT INTO test (token, id) VALUES (:token, :id)"), data3)

        db.execute(sq.text("/* select */ SELECT token FROM test")).fetchall()

        db.execute(sq.text("/* select count */ SELECT COUNT(token) FROM test")).fetchall()

        db.execute(sq.text("/* select order by */ SELECT token FROM test ORDER BY token")).fetchall()

        db.execute(sq.text("/* select where between */ SELECT token FROM test WHERE id BETWEEN 1234 AND 4321")).fetchall()

        db.execute(sq.text("/* select min max avg */ SELECT MIN(id),MAX(id),AVG(id) FROM test")).fetchall()

counter = 1
for i in range(10):
    test(sqlite,counter)
    counter += 1
    test(mysql,counter)
    counter +=1 
    test(postgres,counter)
    counter +=1

print("\nTest Completed! You can now proceed to step eight\n")