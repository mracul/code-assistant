from sqlalchemy import create_engine, inspect

class SQLAnalyzer:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.inspector = inspect(self.engine)

    def get_schema(self):
        """
        Get the schema of the database.
        """
        schema = {}
        for table_name in self.inspector.get_table_names():
            schema[table_name] = []
            for column in self.inspector.get_columns(table_name):
                schema[table_name].append({
                    "name": column['name'],
                    "type": str(column['type']),
                    "nullable": column['nullable'],
                    "default": column['default'],
                })
        return schema
