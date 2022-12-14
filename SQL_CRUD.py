import sys, psycopg2, psycopg2.sql as sql


class SQL_CRUD:
    def __init__(self, user, password, host, port, dbname, table, primarykey=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.table = table
        # self.primarykey = primarykey

    def connect(self):
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname
            )
            cursor = connection.cursor()
            print(
                '------------------------------------------------------------'
                '\n-# PostgreSQL connection & transaction is ACTIVE\n'
            )
        except (Exception, psycopg2.Error) as error:
            print(error, error.pgcode, error.pgerror, sep='\n')
            sys.exit()
        else:
            self._connection = connection
            self._cursor = cursor
            self._counter = 0

    def _check_connection(self):
        try:
            self._connection
        except AttributeError:
            print('ERROR: NOT Connected to Database')
            sys.exit()

    def _execute(self, query, Placeholder_value=None):
        self._check_connection()
        if Placeholder_value == None or None in Placeholder_value:
            self._cursor.execute(query)
            print('-# ' + query.as_string(self._connection) + ';\n')
        else:
            self._cursor.execute(query, Placeholder_value)
            print('-# ' + query.as_string(self._connection) % Placeholder_value + ';\n')

    def commit(self):
        self._check_connection()
        self._connection.commit()
        print('-# COMMIT ' + str(self._counter) + ' changes\n')
        self._counter = 0

    def close(self, commit=False):
        self._check_connection()
        if commit:
            self.commit()
        else:
            self._cursor.close()
            self._connection.close()
        if self._counter > 0:
            print(
                '-# ' + str(self._counter) + ' changes NOT commited  CLOSE connection\n'
                                             '------------------------------------------------------------\n'
            )
        else:
            print(
                '-# CLOSE connection\n'
                '------------------------------------------------------------\n'
            )

    def insert(self, **column_value):
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join(map(sql.Identifier, column_value.keys())),
            sql.SQL(', ').join(sql.Placeholder() * len(column_value.values()))
        )
        record_to_insert = tuple(column_value.values())
        self._execute(insert_query, record_to_insert)
        self._counter += 1

    def get_last_id(self):
        select_query = sql.SQL("SELECT {} from {} order by {} desc limit 1").format(
                sql.Identifier('alert_id'),
                sql.Identifier(self.table),
                sql.Identifier('alert_id')
            )
        self._execute(select_query, )
        try:
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        else:
            print('-# ' + str(selected) + '\n')
            return selected

    def select_all(self, primaryKey_value=None):
        if primaryKey_value == None:
            select_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table))
            self._execute(select_query)
        else:
            select_query = sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier(self.primarykey),
                sql.Placeholder()
            )
            self._execute(select_query, (primaryKey_value,))
        try:
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        else:
            print('-# ' + str(selected) + '\n')
            return selected

    def get_with_email(self, email):
        if email:
            select_query = sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier('email'),
                sql.Placeholder()
            )
            self._execute(select_query, (email,))
            try:
                selected = self._cursor.fetchall()
            except psycopg2.ProgrammingError as error:
                selected = '# ERROR: ' + str(error)
            else:
                print('-# ' + str(selected) + '\n')
                return selected

    def get_all_alerts_with_user(self, user_id):
        if user_id:
            select_query = sql.SQL("SELECT alert_id, crypto_code, trigger_value, status FROM {} WHERE {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier('user_id'),
                sql.Placeholder()
            )
            self._execute(select_query, (user_id,))
            try:
                selected = self._cursor.fetchall()
            except psycopg2.ProgrammingError as error:
                selected = '# ERROR: ' + str(error)
            else:
                print('-# ' + str(selected) + '\n')
                return selected

    def get_all_alerts(self):
        select_query = sql.SQL(
            "SELECT alert_id, crypto_code, trigger_value, status FROM {}").format(
            sql.Identifier(self.table),
        )
        self._execute(select_query, ())
        try:
            selected = self._cursor.fetchall()
        except psycopg2.ProgrammingError as error:
            selected = '# ERROR: ' + str(error)
        else:
            print('-# ' + str(selected) + '\n')
            return selected

    def get_all_alerts_with_status_and_user(self, status, user_id):
        if user_id:
            select_query = sql.SQL(
                "SELECT alert_id, crypto_code, trigger_value, status FROM {} WHERE {} = {} AND {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier('user_id'),
                sql.Placeholder(),
                sql.Identifier('status'),
                sql.Placeholder()
            )
            self._execute(select_query, (user_id, status,))
            try:
                selected = self._cursor.fetchall()
            except psycopg2.ProgrammingError as error:
                selected = '# ERROR: ' + str(error)
            else:
                print('-# ' + str(selected) + '\n')
                return selected

    def update_status_of_alert(self, status, alert_id):
        if alert_id:
            update_query = sql.SQL(
                "UPDATE {} SET {} = {} WHERE {} = {}").format(
                sql.Identifier(self.table),
                sql.Identifier('status'),
                sql.Placeholder(),
                sql.Identifier('alert_id'),
                sql.Placeholder()
            )
            self._execute(update_query, (status, alert_id, ))

# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()
#
#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
#
#         # create a cursor
#         cur = conn.cursor()
#
#         # execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')
#
#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         print(db_version)
#
#         # close the communication with the PostgreSQL
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')
#
#
# if __name__ == '__main__':
#     connect()
