import sqlite3
from typing import Optional, List, Dict, Any, Union

class Database:
        
    def execute(db, query: str, params: tuple = ()) -> List[Dict]:
        """Выполняет SQL запрос и возвращает результат в виде списка словарей"""
        try:
            db.cursor.execute(query, params)
            db.conn.commit()
            return db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def table_cols(db, table: str) -> list[str]:
        sql = f"SELECT c.name FROM pragma_table_info('{table}') as c;"
        return list(map(lambda row: row[0], Database.select(sql)))
    
    def rows_to_dicts(col_names: list[str], rows: list[tuple]) -> list[dict[str, Any]]:
        data = []
        for row in rows:
            dict_row = {col: val for val, col in zip(row, col_names)}
            data.append(dict_row)
        return data

    # INSERT методы
    def insert(db, table: str, data: Dict) -> int:
        """
        Вставляет одну запись в таблицу
        
        Args:
            table: Имя таблицы
            data: Словарь {имя_колонки: значение}
            
        Returns:
            ID вставленной записи
        """
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ', '.join(['?'] * len(columns))
        
        query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders});
        """
        
        db.cursor.execute(query, values)
        db.conn.commit()
        return db.cursor.lastrowid
    
    def insert_many(db, table: str, columns: List[str], data: List[tuple]) -> None:
        """
        Вставляет несколько записей за один раз
        
        Args:
            table: Имя таблицы
            columns: Список колонок
            data: Список кортежей с значениями
        """
        placeholders = ', '.join(['?'] * len(columns))
        query = f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders});
        """
        
        db.cursor.execute(query, data)
        db.conn.commit()

    # SELECT методы
    def select(db, table: str, columns: Union[List[str], str] = "*", 
              where: Optional[str] = None, params: tuple = ()) -> List[Dict]:
        """
        Выполняет SELECT запрос
        
        Args:
            table: Имя таблицы
            columns: Список колонок или "*" для всех
            where: Условие WHERE (без самого слова WHERE)
            params: Параметры для условия
            
        Returns:
            Список словарей с результатами
        """
        if isinstance(columns, list):
            columns_str = ', '.join(columns)
        else:
            columns_str = columns
            
        query = f"SELECT {columns_str} FROM {table}"
        
        if where:
            query += f" WHERE {where}"
            
        query += ";"
        
        return Database.rows_to_dicts(columns, db.execute(query, params))
    
    def select_one(db, table: str, columns: Union[List[str], str] = "*", 
                  where: Optional[str] = None, params: tuple = ()) -> Optional[Dict]:
        """
        Возвращает одну запись или None
        """
        result = db.select(table, columns, where, params)
        return result[0] if result else None

    # UPDATE методы
    def update(db, table: str, data: Dict, where: str, params: tuple = ()) -> int:
        """
        Обновляет записи в таблице
        
        Args:
            table: Имя таблицы
            data: Словарь {колонка: новое_значение}
            where: Условие WHERE (без самого слова WHERE)
            params: Дополнительные параметры для условия
            
        Returns:
            Количество измененных строк
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        values = list(data.values()) + list(params)
        
        query = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE {where};
        """
        
        db.cursor.execute(query, values)
        db.conn.commit()
        return db.cursor.rowcount

    # DELETE методы
    def delete(db, table: str, where: str, params: tuple = ()) -> int:
        """
        Удаляет записи из таблицы
        
        Args:
            table: Имя таблицы
            where: Условие WHERE (без самого слова WHERE)
            params: Параметры для условия
            
        Returns:
            Количество удаленных строк
        """
        query = f"DELETE FROM {table} WHERE {where};"
        db.cursor.execute(query, params)
        db.conn.commit()
        return db.cursor.rowcount