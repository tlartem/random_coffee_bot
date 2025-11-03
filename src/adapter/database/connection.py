from shared.db_helper import DatabaseHelper
from src.config import settings

db_helper = DatabaseHelper(url=str(settings.db.url))

session_getter = db_helper.session_getter
get_session = db_helper.get_session
close_db_connection = db_helper.dispose
create_tables = db_helper.create_tables
