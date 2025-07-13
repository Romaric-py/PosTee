from db_manager import DBManager
from pprint import pprint

db_manager = DBManager()

result = db_manager.fetch_all(
    """
        SELECT * 
        FROM friendships
    """
)

for row in result:
    pprint(dict(row), indent=4, sort_dicts=False)
    print()
    