import aiosqlite

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None 

    async def connect(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_name)
        return self.connection
    
    async def close_connect(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def create_table(self, table_name, columns):
        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        db = await self.connect()
        await db.execute(query)
        await db.commit()

    async def add_new(self, table_name, values):
        placeholders = ", ".join(["?"] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        db = await self.connect()
        await db.execute(query, values)
        await db.commit()

    async def select_values(self, table_name, columns):
        columns_str = ", ".join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        db = await self.connect()
        async with db.execute(query) as cursor:
            return await cursor.fetchall()

    async def delete_values(self, table_name):
        query = f"DELETE FROM {table_name}"
        db = await self.connect()
        await db.execute(query)
        await db.commit()

    async def edit_value(self, table_name, key, new_value, search_key, value):
        query = f"UPDATE {table_name} SET {key} = ? WHERE {search_key} = ?"
        db = await self.connect()
        await db.execute(query, (new_value, value))
        await db.commit()

    async def load_data_from_db(self, table_name, model_class):
        rows = await self.select_values(table_name, ["*"])
        return [model_class(*row) for row in rows]
