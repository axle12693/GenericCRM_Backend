import psycopg2
import json
from datetime import datetime


class Module:
    def __init__(self, config):
        self.config = config
        self.conn = psycopg2.connect(
            dbname=self.config.db_name,
            user=self.config.db_user,
            password=self.config.db_password,
            host=self.config.db_host,
            port=self.config.db_port
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:

            cur.execute('''CREATE TABLE IF NOT EXISTS Module (
                                module_id SERIAL PRIMARY KEY,
                                module_name TEXT NOT NULL,
                                UNIQUE (module_name)
                            );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS Field (
                                field_id SERIAL PRIMARY KEY,
                                module_id INTEGER NOT NULL,
                                field_name TEXT NOT NULL,
                                data_type TEXT NOT NULL,
                                FOREIGN KEY (module_id) REFERENCES Module(module_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                UNIQUE (module_id, field_name)
                            );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS Instance (
                                instance_id SERIAL PRIMARY KEY,
                                module_id INTEGER NOT NULL,
                                FOREIGN KEY (module_id) REFERENCES Module(module_id) ON DELETE CASCADE ON UPDATE CASCADE
                            );''')

            cur.execute('''CREATE TABLE IF NOT EXISTS FieldEntry (
                                field_entry_id SERIAL PRIMARY KEY,
                                instance_id INTEGER NOT NULL,
                                field_id INTEGER NOT NULL,
                                value TEXT NOT NULL,
                                FOREIGN KEY (field_id) REFERENCES Field(field_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (instance_id) REFERENCES Instance(instance_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                UNIQUE (instance_id, field_id)
                            );''')
            self.conn.commit()

    def create_field(self, module_id, field_name, data_type):
        with self.conn.cursor() as cur:
            cur.execute('INSERT INTO Field (module_id, field_name, data_type) VALUES (%s, %s, %s)', (module_id, field_name, data_type))
            self.conn.commit()

    def set_field_value(self, instance_id, field_id, value):
        with self.conn.cursor() as cur:
            cur.execute('SELECT data_type FROM Field WHERE field_id = %s', (field_id,))
            field = cur.fetchone()
            if not field:
                raise ValueError(f"Field '{field_id}' does not exist.")

            data_type = field[0]
            value_str = self._serialize_value(value, data_type)

            cur.execute('INSERT INTO FieldEntry (instance_id, field_id, value) VALUES (%s, %s, %s)',
                        (instance_id, field_id, value_str))
            self.conn.commit()

    def get_field_value(self, instance_id, field_id):
        with self.conn.cursor() as cur:
            cur.execute('SELECT data_type FROM Field WHERE field_id = %s', (field_id,))
            field = cur.fetchone()
            if not field:
                raise ValueError(f"Field '{field_id}' does not exist.")

            data_type = field[0]
            cur.execute('SELECT value FROM FieldEntry WHERE instance_id = %s AND field_id = %s',
                        (instance_id, field_id))
            value_str = cur.fetchone()
            if not value_str:
                return None

            return self._deserialize_value(value_str[0], data_type)

    def _serialize_value(self, value, data_type):
        if data_type == 'text':
            return json.dumps({'type': 'text', 'value': value})
        elif data_type == 'integer':
            return json.dumps({'type': 'integer', 'value': value})
        elif data_type == 'boolean':
            return json.dumps({'type': 'boolean', 'value': value})
        elif data_type == 'date':
            return json.dumps({'type': 'date', 'value': value.strftime('%Y-%m-%d')})
        else:
            raise ValueError(f"Unsupported data type '{data_type}'.")

    def _deserialize_value(self, value_str, data_type):
        value_json = json.loads(value_str)
        if data_type == 'text':
            return value_json['value']
        elif data_type == 'integer':
            return int(value_json['value'])
        elif data_type == 'boolean':
            return value_json['value'] == 'true'
        elif data_type == 'date':
            return datetime.strptime(value_json['value'], '%Y-%m-%d')
        else:
            raise ValueError(f"Unsupported data type '{data_type}'.")
