import mysql.connector
import os, time

config = {
    'host': 'localhost',
    'database': None,
    'user': 'root',
    'password': 'password',
}

def main():
    connect_database = False
    while True:
        os.system('clear')
        try:
            database = input('Enter a database name or press 9 to quit: ')
            if database == '9':
                print('Exiting...')
                time.sleep(2)
                os.system('clear')
                break
            config['database'] = database
            connection = mysql.connector.connect(**config)
            if connection.is_connected():
                print(f'Connected to {database} database')
                connect_database = True
                time.sleep(2)
        except mysql.connector.Error as err:
            print(f'Error: {err}. Not connected to {database} database')
            time.sleep(2)

        if not connect_database:
            continue

        while True:
            menu = input('1:Select\n2:Insert\n3:Update\n4:Delete\n9:Exit\n>>>')
            os.system('clear')
            if menu == '1':
                print('What table do you want to select from?: ')
                cursor = connection.cursor()
                cursor.execute('SHOW TABLES')
                tables = cursor.fetchall()
                count = 1
                for table in tables:
                    print(f'{count}:{table[0]}')
                    count += 1
                table_number = input('Choose table number: ')
                table_name = tables[int(table_number) - 1][0]
                cursor.execute(f'SHOW COLUMNS FROM {table_name}')
                columns_info = [column[0] for column in cursor.fetchall()]
                print()
                print('What columns do you want to select? (comma-separated): ')
                print(', '.join(columns_info))
                print()
                selected_columns = input('Enter column names: ')
                
                cursor.execute(f'SELECT {selected_columns} FROM {table_name}')
                rows = cursor.fetchall()
                for row in rows:
                    for i, column_value in enumerate(row):
                        print(f'{columns_info[i]}: {column_value}')
                cursor.close()
            elif menu == '2':
                print('What table do you want to insert into?: ')
                cursor = connection.cursor()
                cursor.execute('SHOW TABLES')
                tables = cursor.fetchall()
                count = 1
                for table in tables:
                    print(f'{count}:{table[0]}')
                    count += 1
                table_number = input('Choose table number to insert into: ')
                table_name = tables[int(table_number) - 1][0]
                cursor.execute(f'SHOW COLUMNS FROM {table_name}')
                columns_info = [column[0] for column in cursor.fetchall()]

                # Allow the user to enter values for each column
                values = {}
                for column in columns_info:
                    value = input(f'Enter value for {column}: ')
                    values[column] = value

                # Construct the INSERT statement
                columns = ', '.join(values.keys())
                column_values = ', '.join(f"'{value}'" for value in values.values())
                insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({column_values})'

                # Execute the INSERT statement
                try:
                    cursor.execute(insert_query)
                    connection.commit()
                    print('Data successfully inserted.')
                except mysql.connector.Error as err:
                    print(f'Error: {err}. Failed to insert data.')
                cursor.close()
            elif menu == '3':
                print('What table do you want to update?: ')
                cursor = connection.cursor()
                cursor.execute('SHOW TABLES')
                tables = cursor.fetchall()
                count = 1
                for table in tables:
                    print(f'{count}:{table[0]}')
                    count += 1
                table_number = input('Choose table number to update: ')
                table_name = tables[int(table_number) - 1][0]
                cursor.execute(f'SHOW COLUMNS FROM {table_name}')
                columns_info = [column[0] for column in cursor.fetchall()]

                # Allow the user to enter values for each column
                values = {}
                for column in columns_info:
                    value = input(f'Enter value for {column}: ')
                    values[column] = value

                # Prompt the user for the primary key value
                primary_key_column = input('Enter the primary key column: ')
                primary_key_value = input(f'Enter value for {primary_key_column} to identify the record: ')

                # Construct the UPDATE statement
                columns = ', '.join(f'{key} = \'{value}\'' for key, value in values.items())
                update_query = f'UPDATE {table_name} SET {columns} WHERE {primary_key_column} = \'{primary_key_value}\''

                # Execute the UPDATE statement
                try:
                    cursor.execute(update_query)
                    connection.commit()
                    print('Data successfully updated.')
                except mysql.connector.Error as err:
                    print(f'Error: {err}. Failed to update data.')
                finally:
                    cursor.close()
                            
            elif menu == '4':
                print('What table do you want to delete from?: ')
                cursor = connection.cursor()
                cursor.execute('SHOW TABLES')
                tables = cursor.fetchall()
                count = 1
                for table in tables:
                    print(f'{count}:{table[0]}')
                    count += 1
                table_number = input('Choose table number to delete from: ')
                table_name = tables[int(table_number) - 1][0]
                cursor.execute(f'SHOW COLUMNS FROM {table_name}')
                columns_info = [column[0] for column in cursor.fetchall()]

                # Prompt the user for the primary key value
                primary_key_column = input('Enter the primary key column: ')
                primary_key_value = input(f'Enter value for {primary_key_column} to identify the record: ')

                # Construct the DELETE statement
                delete_query = f'DELETE FROM {table_name} WHERE {primary_key_column} = \'{primary_key_value}\''

                # Execute the DELETE statement
                try:
                    cursor.execute(delete_query)
                    connection.commit()
                    print('Data successfully deleted.')
                except mysql.connector.Error as err:
                    print(f'Error: {err}. Failed to delete data.')
                finally:
                    cursor.close()
            elif menu == '9':
                connection.close()
                print('Connection closed')
                print('Goin back to main menu')
                time.sleep(2)
                break


if __name__ == '__main__':
    main()