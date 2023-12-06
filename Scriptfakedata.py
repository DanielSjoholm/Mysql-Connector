from faker import Faker
import mysql.connector
import os, time

fake = Faker()

config = {
    'host': 'localhost',
    'database': None,
    'user': 'root',
    'password': 'password',
}

generated_personnummers = set()

def generate_unique_personnummer():
    # Generate a unique 10-digit number
    while True:
        personnummer = str(fake.random_number(digits=10, fix_len=True))
        if personnummer not in generated_personnummers:
            generated_personnummers.add(personnummer)
            return personnummer


def generate_fake_student():
    # This function needs to be adapted to your database schema
    # Replace 'some_other_attribute' with the actual field names and methods to generate them
    return {
        'Personnummer': generate_unique_personnummer(),
        'StudentNamn': fake.name(),
        'SkolID': 1
    }

def insert_students(cursor, batch_size):
    insert_query = """
    INSERT INTO Student (Personnummer, StudentNamn, SkolID) VALUES (%s, %s, %s)
    """
    # Create a batch of student data
    students_data = []
    for _ in range(batch_size):
        student = generate_fake_student()  # Generate a single student's data
        students_data.append((student['Personnummer'], student['StudentNamn'], student['SkolID']))

    # Use executemany to insert the batch
    cursor.executemany(insert_query, students_data)

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
            if menu == '2':
                cursor = connection.cursor()
                batch_size = 2000  # Set a reasonable batch size
                num_batches = 2000  # Set the number of batches to reach 1,000,000 records

                for _ in range(num_batches):
                    insert_students(cursor, batch_size)
                    connection.commit()  # Commit after each batch to avoid a huge transaction
                    print(f'Inserted {batch_size} students, committing changes...')

                cursor.close()
                print(f'Finished inserting {batch_size * num_batches} students.')
            # ...

if __name__ == '__main__':
    main()
