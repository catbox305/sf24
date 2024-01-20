import sqlalchemy as sq
from sqlalchemy import (
    create_engine,
)
import time, random

strings = ["".join(random.choices("q w e r t y u i o p a s d f g h j k l z x c v b n m".split(),k=20)) for i in range(100000)]
data = [{"string":i} for i in strings]

db = sq.create_engine("sqlite+pysqlite:///sqlite3.db",echo=True)
with db.connect() as con:

    @sq.event.listens_for(db, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(time.time())
        print("Start Query:", statement)


    @sq.event.listens_for(db, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        print("Query Complete!")
        print("\033[38;2;0;255;255mTotal Time:", str(total)+"s\033[0m")


    con.execute("CREATE TABLE test (string varchar(100))")
    con.execute("INSERT INTO test VALUES (:string)",data)
    con.execute("DROP TABLE test")