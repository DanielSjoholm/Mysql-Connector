from faker import Faker
import mysql.connector
import os, time

fake = Faker()

config = {
    'host': 'localhost',
    'database': 'Studentregister',
    'user': 'root',
    'password': 'password',
}

def assign_students_to_course(connection, cursor, kurs_ids):
    cursor.execute("SELECT Personnummer FROM Student")
    student_personnummers = cursor.fetchall()

    counter = 1
    for personnummer in student_personnummers:
        for kurs_id in kurs_ids:
            # Check if the entry already exists
            cursor.execute("""
                SELECT COUNT(1) FROM StudentKursBridge WHERE Personnummer = %s AND KursID = %s
            """, (personnummer[0], kurs_id))
            if cursor.fetchone()[0] == 0:  # If the entry does not exist
                insert_query = """
                INSERT INTO StudentKursBridge (Personnummer, KursID) VALUES (%s, %s)
                """
                cursor.execute(insert_query, (personnummer[0], kurs_id))
                connection.commit()  # Commit after the INSERT
                print(f"{counter}: Insert accepted for student {personnummer[0]} into kurs {kurs_id}")
            else:
                print(f"Student {personnummer[0]} is already assigned to course {kurs_id}, skipping.")
            counter += 1




def main():
    os.system('clear')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f'Connected')
            time.sleep(2)
    except mysql.connector.Error as err:
        print(f'Error: {err}. Not connected database')
        time.sleep(2)
    while True:
        menu = input('1:Insert')
        start_time = time.time() 
        os.system('clear')
        if menu == '1':
            cursor = connection.cursor()
            # Define the course IDs to assign every student to
            kurs_ids = [1, 2]
            assign_students_to_course(connection,cursor, kurs_ids)
            connection.commit()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'All students have been assigned to courses {kurs_ids}.')
            print(f"Operation took {elapsed_time:.2f} seconds.") 
            cursor.close()

if __name__ == '__main__':
    main()
