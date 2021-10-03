import sqlite3


class Database:
    def __init__(self):
        self.db_name = "project_db.db"
        self.conn = sqlite3.connect(self.db_name,check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS "catalog_category"(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         parent_id INTEGER DEFAULT NULL,
         FOREIGN KEY (parent_id) REFERENCES catalog_category(id)
         ON UPDATE CASCADE  ON DELETE CASCADE
        )
        """)
        self.conn.execute("""
          CREATE TABLE IF NOT EXISTS "catalog_types"(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL
            )
        """)
        self.conn.execute("""
         CREATE TABLE IF NOT EXISTS "catalog_product"(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         price INTEGER NOT NULL,
         description TEXT NOT NULL,
         photo TEXT NOT NULL,
         category_id INTEGER NOT NULL,
         type_id INTEGER NOT NULL,
         FOREIGN KEY (category_id)  REFERENCES catalog_category(id)
         ON UPDATE CASCADE ON DELETE CASCADE,
         FOREIGN KEY (type_id) REFERENCES catalog_types(id)
         ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
        self.conn.commit()
    def get_menu(self):
        data = self.conn.execute("""
        SELECT id,name FROM "catalog_category"
        WHERE parent_id is null
        """).fetchall()
        return data
    def get_menu_child(self,data):
        product = self.conn.execute(f""" SELECT id,name FROM "catalog_category"
        WHERE parent_id = "{data}"  
        """).fetchall()
        return product
    def get_type(self,category_id):
        types = self.conn.execute(f"""
            select catalog_types.id as id ,catalog_types.name as name FROM "catalog_types"
            inner Join "catalog_product"
            On catalog_types.id = catalog_product.type_id
            where catalog_product.category_id = ?
        """,[category_id]).fetchall()
        return types
    def get_product(self,category_id,type_id):
        product = self.conn.execute("""
        select * from catalog_product 
        where category_id = ? and type_id = ?
        """,[category_id,type_id]).fetchone()
        return product
    def get_product_by_id(self,product_id):
        product = self.conn.execute("""
               select * from catalog_product 
               where id = ?
               """, [product_id]).fetchone()
        return product
    def add(self):
        category = [
            (1, '🌯 Lavash', None),
            (2, '🥙 Shaurma', None),
            (3, '🍲 Donar', None),
            (4, '🍔 Burger', None),
            (5, '🌭 Xot-Dog', None),
            (6, '🍰 Desertlar', None),
            (7, '☕️ Ichimliklar', None),
            (8, '🍟 Gazaklar', None)
        ]
        type = [
            (1, 'mini'),
            (2, 'klassik'),
        ]
        self.conn.executemany("""
        INSERT INTO "catalog_category" 
        VALUES(?,?,?)
        """,category)
        self.conn.executemany("""
                INSERT INTO "catalog_types" 
                VALUES(?,?)
                """, type)
        self.conn.commit()

