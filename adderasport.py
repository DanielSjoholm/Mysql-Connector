from faker import Faker
import mysql.connector
import os, time
import random

fake = Faker()

config = {
    'host': 'localhost',
    'database': 'Studentregister',
    'user': 'root',
    'password': 'password',
}

def assign_students_to_sport(connection, cursor, sport_ids):
    cursor.execute("SELECT Personnummer FROM Student")
    student_personnummers = cursor.fetchall()  # This will be a list of tuples
    
    counter = 1  # Initialize a counter to keep track of the insertions
    for personnummer in student_personnummers:
        sport_id = random.choice(sport_ids)  # Randomly choose either SportID 1 or 2
        try:
            insert_query = """
            INSERT INTO StudentSportBridge (Personnummer, SportID) VALUES (%s, %s)
            """
            cursor.execute(insert_query, (personnummer[0], sport_id))
            connection.commit()  # Commit the transaction immediately after the insert
            print(f"{counter}: Insert accepted for student {personnummer[0]} into sport {sport_id}")
            counter += 1  # Increment the counter after each successful insert
        except mysql.connector.Error as err:
            # If an error occurs, roll back the transaction
            connection.rollback()
            print(f"Error: {err}. Could not assign student {personnummer[0]} to sport {sport_id}.")

            time.sleep(2)


def main():
    os.system('clear')
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f'Connected')
            time.sleep(2)
    except mysql.connector.Error as err:
        print(f'Error: {err}. Not connected')
        time.sleep(2)
    while True:
        menu = input('1:Insert\n2:Exit\n>>>')
        start_time = time.time() 
        os.system('clear')
        if menu == '1':
            start_time = time.time()  # Start the timer
            cursor = connection.cursor()

            # Define the sport IDs to randomly assign each student to one of them
            sport_ids = [1, 2]
            assign_students_to_sport(connection, cursor, sport_ids)

            connection.commit()
            end_time = time.time()  # End the timer
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f'All students have been randomly assigned to sports {sport_ids}.')
            print(f"Operation took {elapsed_time:.2f} seconds.")
            cursor.close()
        elif menu == '2':
            break


if __name__ == '__main__':
    main()
