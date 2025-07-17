from db_manager import DBManager
from pprint import pprint

db_manager = DBManager()

db_manager.execute_sql_file('./db_manager/generate.sql')
db_manager.execute_sql_file('./db_manager/seed.sql')

result = db_manager.fetch_all(
    """
        SELECT * 
        FROM friendships
    """
)

for row in result:
    pprint(dict(row), indent=4, sort_dicts=False)
    print()
    