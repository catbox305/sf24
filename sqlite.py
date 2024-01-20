import aiosqlite
import time
import random
import asyncio

#print('\033[0;0H',end='')
#print('\033[2J',end='')

async def test():

    strings = ["".join(random.choices("q w e r t y u i o p a s d f g h j k l z x c v b n m".split(),k=20)) for i in range(100000)]
    data = [
        {"strings":strings[i]} for i in range(100000)
    ]


    start_ = time.time()

    start=time.time()
    con = await aiosqlite.connect("sqlite3.db")
    #print("├─ Connect               → "+str(time.time()-start)+"s") # |- 1

    start=time.time()
    cur = await con.cursor()
    #print("├─ Define cursor         → "+str(time.time()-start)+"s") # |- 2

    start=time.time()
    await cur.execute("CREATE TABLE test(string varchar(100))")
    print("├─ Make a table           → "+str(time.time()-start)+"s") # |- 3

    start=time.time()
    #tmp = str("".join((random.choice("qwertyuiopasdfghjklzxcvbnm".split()) for i in range(10))))
    await cur.executemany("INSERT INTO test(string) VALUES (:strings)",data)
    await con.commit()
    print("├─ Insert 100,000 strings → "+str(time.time()-start)+"s") # |- 4

    start=time.time()
    await cur.execute("SELECT string FROM test")
    print("├─ Read the strings       → "+str(time.time()-start)+"s") # |- 3

    await con.close()
    end_ = time.time()

    print("│")
    print("└── Total time            → "+str(end_-start_)+"s") # |___ end

asyncio.run(test())