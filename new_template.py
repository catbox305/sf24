import sys
import time
import asyncio
import sqlalchemy as sq
import random




"""
gui=[
f"\033[0;0H\033[2J",
f"╭─postgresql───╶╴───{aaa}.{bb}s─╮",
f"├┐                          │",
f"{CC}read them         {ccc}.{dd}s │",
f"{BC}                          │",
f"{BB}add 100k strings  {eee}.{ff}s │",
f"{AB}                          │",
f"{AA}make a table      {ggg}.{hh}s │",
f"├┘                          │",
f"╰───────────────────────────╯",
]
print("\n".join(gui))
"""
class Gui:
    def __init__(self,nm):

        self.nm = nm

        self.closed = "\033[38;2;70;255;0m├┤\033[0m"
        self.opened = "\033[38;2;255;70;0m││\033[0m"

        self.c = ["xx", "xxx"]

        self.meter = 0
        self.t = [
            ["xx","xxx"] for i in range(6)
        ]
    def update(self):

        tmp = [[self.closed for i in range(self.meter)],[self.opened for i in range(6-self.meter)]]
        tmp = tmp[0]+tmp[1]

        print("\n".join([
            f"\033[0;0H\033[2J",
            f"╭─{self.nm}───╶╴───{self.c[0]}.{self.c[1]}s─╮",
            f"├┐                          │",
            f"{tmp[5]}index             {self.t[5][0]}.{self.t[5][1]}s │",
            f"{tmp[4]}count             {self.t[4][0]}.{self.t[4][1]}s │",
            f"{tmp[3]}order by          {self.t[3][0]}.{self.t[3][1]}s │",
            f"{tmp[2]}min, max, avg     {self.t[2][0]}.{self.t[2][1]}s │",
            f"{tmp[1]}read the strings  {self.t[1][0]}.{self.t[1][1]}s │",
            f"{tmp[0]}add 100k strings  {self.t[0][0]}.{self.t[0][1]}s │",
            f"├┘                          │",
            f"╰───────────────────────────╯",
        ]))

class DualGui:
    def __init__(self,nm1,nm2):

        self.nm = [nm1,nm2]

        self.closed = "\033[38;2;70;255;0m├┤\033[0m"
        self.opened = "\033[38;2;255;70;0m││\033[0m"

        self.c = [["xx","xxx"],["xx","xxx"]]

        self.meter = [0,0]

        self.t = [[["xx","xxx"] for i in range(5)],[["xx","xxx"] for i in range(5)]]
    def update(self):

        tmp1 = [[self.closed for i in range(self.meter[0])],[self.opened for i in range(5-self.meter[0])]]
        tmp1 = tmp1[0]+tmp1[1]
        tmp2 = [[self.closed for i in range(self.meter[1])],[self.opened for i in range(5-self.meter[1])]]
        tmp2 = tmp2[0]+tmp2[1]

        print("\n".join([
            f"\033[0;0H\033[2J",
            f"╭─{self.nm[0]}───╶╴───{self.c[0][0]}.{self.c[0][1]}s─╮ "+f" ╭─{self.nm[1]}───╶╴───{self.c[1][0]}.{self.c[1][1]}s─╮",
            f"├┐                          │ "+f" ├┐                          │",
            f"{tmp1[4]}where, index      {self.t[0][4][0]}.{self.t[0][4][1]}s │ "+f" {tmp2[4]}where, index      {self.t[1][4][0]}.{self.t[1][4][1]}s │",
            f"{tmp1[3]}order by, count   {self.t[0][3][0]}.{self.t[0][3][1]}s │ "+f" {tmp2[3]}order by, count   {self.t[1][3][0]}.{self.t[1][3][1]}s │",
            f"{tmp1[2]}min, max, avg     {self.t[0][2][0]}.{self.t[0][2][1]}s │ "+f" {tmp2[2]}min, max, avg     {self.t[1][2][0]}.{self.t[1][2][1]}s │",
            f"{tmp1[1]}read them         {self.t[0][1][0]}.{self.t[0][1][1]}s │ "+f" {tmp2[1]}read them         {self.t[1][1][0]}.{self.t[1][1][1]}s │",
            f"{tmp1[0]}add 100k strings  {self.t[0][0][0]}.{self.t[0][0][1]}s │ "+f" {tmp2[0]}add 100k strings  {self.t[1][0][0]}.{self.t[1][0][1]}s │",
            f"├┘                          │ "+f" ├┘                          │",
            f"╰───────────────────────────╯ "+f" ╰───────────────────────────╯",
        ]))

def test(wdb):



    if wdb == [wdb[0],"sqlite"]:
        _db = sq.create_engine("sqlite+pysqlite:///sqlite3.db", echo=True); nm = "──sqlite──"
        mode = 1
    elif wdb == [wdb[0],"pg"]:
        _db = sq.create_engine("postgresql+asyncpg://localhost/lion"); nm = "postgresql"
        mode = 1
    elif wdb == [wdb[0],"sqlite","pg"] or wdb == [wdb[0],"pg","sqlite"]:
        db1 = sq.create_engine("sqlite+pysqlite:///sqlite3.db"); nm1 = "──sqlite──"
        db2 = sq.create_engine("postgresql+asyncpg://localhost/lion"); nm2 = "postgresql"
        mode = 2

    else:
        return
    
    print("Waiting...")

    strings = ["".join(random.choices("q w e r t y u i o p a s d f g h j k l z x c v b n m".split(),k=20)) for i in range(100000)]
    data = [{"string":i} for i in strings]

    if mode == 1:

        db = _db.connect()

        global gui
        gui = Gui(nm)

        db.execute("DROP TABLE IF EXISTS test")
        db.execute("CREATE TABLE test (string varchar(100))")

        @sq.event.listens_for(db, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault("query_start_time", []).append(time.time())
            print("Start Query:", statement)


        @sq.event.listens_for(db, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total = time.time() - conn.info["query_start_time"].pop(-1)
            global gui
            #tmp=total+float(".".join([gui.t[gui.meter][0],gui.t[gui.meter][1]]).replace("x","0"))
            tmp=f"{total:.6f}".split(".")

            gui.t[gui.meter][0] = tmp[0].rjust(2)
            gui.t[gui.meter][1] = tmp[1][0:3]
            print("Query Complete!", statement)
            print("\033[38;2;0;255;255mTotal Time:", str(total)+"s\033[0m")

        gui.update()

        start_ = time.time()





        start=time.time()
        db.execute("INSERT INTO test (string) VALUES (:string)", data)
        '''
        tmp=str(total).split(".")
        gui.t[gui.meter][0] = tmp[0].rjust(2)
        gui.t[gui.meter][1] = tmp[1][0:3]
        '''
        gui.meter +=1
        #gui.update()

        start=time.time()
        db.execute("SELECT string FROM test").fetchall()
        
        gui.meter +=2
        #gui.update()


        db.execute("SELECT COUNT(string) FROM test")
        gui.meter+=1
        db.execute("SELECT string FROM test ORDER BY string")

        gui.meter +=1
        #gui.update()

        db.close()
        end_=time.time()
        tmp=str(end_-start_).split(".")
        gui.c[0] = tmp[0]; gui.c[0]=str("─"*(2-len(tmp[0])))+gui.c[0]
        gui.c[1] = tmp[1][0:3]
        #gui.update()
        return
    
    elif mode == 2:

        gui = DualGui(nm1,nm2)
        #gui.update()
        db = [db1,db2]
        
        for i in range(2):

            start_ = time.time()

            db[i].connect()

            db[i].execute(query="CREATE TABLE test (string varchar(100))")

            start=time.time()

            db[i].execute(query="INSERT INTO test (string) VALUES (:string)", values=data)

            tmp=str(time.time()-start).split(".")
            gui.t[i][gui.meter[i]][0] = tmp[0].rjust(2)
            gui.t[i][gui.meter[i]][1] = tmp[1][0:3]

            gui.meter[i] +=1
            #gui.update()

            start=time.time()
            #db[i].fetch_all(query="SELECT string FROM test")

            tmp=str(time.time()-start).split(".")
            gui.t[i][gui.meter[i]][0]=str(" "*(2-len(tmp[0])))+tmp[0]
            gui.t[i][gui.meter[i]][1] = tmp[1][0:3]
            
            gui.meter[i] +=2
            gui.update()

            start=time.time()
            db[i].fetch_all(query="SELECT string FROM test ORDER BY string")
            db[i].fetch_one(query="SELECT COUNT(string) FROM test")
            tmp=str(time.time()-start).split(".")
            gui.t[i][gui.meter[i]][0]=str(" "*(2-len(tmp[0])))+tmp[0]
            gui.t[i][gui.meter[i]][1] = tmp[1][0:3]
            
            gui.meter[i] +=1
            gui.update()



            # Close all connections in the connection pool
            db[i].disconnect()

            end_=time.time()
            tmp=str(end_-start_).split(".")
            gui.c[i][0] = tmp[0]; gui.c[i][0]=str("─"*(2-len(tmp[0])))+gui.c[i][0]
            gui.c[i][1] = tmp[1][0:3]
            gui.update()

test(sys.argv)