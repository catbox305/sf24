import sqlalchemy as sq

test = sq.create_engine("sqlite+pysqlite:///data.db")

with test.connect() as db:
    while True:
        try:
            query = input("┌╴")
        except KeyboardInterrupt:
            break

        try:
            result = db.execute(sq.text(query))
            for row in result.fetchall():
                print("├╴"+str(row))
            print("└─"+"─"*len(query))
        except Exception as e:
            print(e)
