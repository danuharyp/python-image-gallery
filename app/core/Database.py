from app.database import con, cur


class Database:

    def __init__(self):
        self.db = con
        self.cursor = cur
