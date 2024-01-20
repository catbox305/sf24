from databases import Database
import time
import asyncio
import sys

async def test(wdb):

    if wdb == "sqlite":
        db = Database("sqlite+aiosqlite://sqlite3.db", force_rollback=True); nm = "sqlite"
    elif wdb == "pg":
        db = Database("postgresql+aiopg://localhost/lion", force_rollback=True); nm = "postgresql"
    else:
        return
    
    print(nm)
    print("│")

    start_ = time.time()

    # Establish the connection pool
    await db.connect()

    print("├─ Make a table           → ",end="",flush=True) #

    start=time.time()
    await db.execute(query="CREATE TABLE test(string char(13))")
    print(str(time.time()-start)[0:6]+"s") # |- 3

    
    print("├─ Insert 100,000 strings → ",end="",flush=True) #

    values=[{"string":"Hello, World!"} for i in range(100000)]
    start=time.time()

    await db.execute_many(query="INSERT INTO test(string) VALUES (:string)",values=values)
    print(str(time.time()-start)[0:6]+"s") # |- 4


    print("├─ Read the strings       → ",end="",flush=True) #

    start=time.time()
    res = await db.fetch_all(query="SELECT string FROM test")
    print(str(time.time()-start)[0:6]+"s") # |- 3

    # Close all connections in the connection pool
    await db.disconnect()

    end_=time.time()

    print("│")
    print("└── Total time            → "+str(end_-start_)[0:6]+"s") #


asyncio.run(test(sys.argv[1]))