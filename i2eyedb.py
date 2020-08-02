# DB connection
import psycopg2
from psycopg2 import Error, extras
import csv
import json
import requests

from flask import Flask
app = Flask(__name__)

# Route for front end to send GET requests to retrieve all questions from the database in JSON format.
@app.route('/get_questions', methods=["GET"])
def get_all_questions():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor2 = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor3 = connection.cursor()
        postgres_select_query = """ SELECT station_id FROM station"""
        cursor.execute(postgres_select_query)
        connection.commit()
        station_id_list = cursor.fetchall()
        print(station_id_list)
        results = {}
        for i in station_id_list:
            station_id, = i
            postgres_select_query = """SELECT question_id, question, type_id FROM question WHERE station_id = {0}""".format(station_id)
            postgres_select_query2 = """SELECT station_name FROM station WHERE station_id = {0}""".format(station_id)
            cursor3.execute(postgres_select_query2)
            station_name, = cursor3.fetchall()[0]
            cursor2.execute(postgres_select_query)
            connection.commit()
            
            results.update({station_name : cursor2.fetchall()})
            # print(results)
            print("Successful query of question table.")
        return json.dumps(results)
  
      # ^ {"Registration": [
      #     {"question_id": 1, "question": "Name", "type_id": 1}, 
      #     {"question_id": 2, "question": "Gender", "type_id": 2}, 
      #     {"question_id": 3, "question": "Age", "type_id": 3}, 
      #     {"question_id": 4, "question": "Birthday", "type_id": 4}
      #     ]
      # }
      
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while getting question table and converting to JSON.", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# get patient data from the patient id
@app.route('/get_data', methods=["GET"])
def get_patient_data(patient_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor2 = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor3 = connection.cursor()
        postgres_select_query = """ SELECT station_id FROM station"""
        cursor.execute(postgres_select_query)
        connection.commit()
        station_id_list = cursor.fetchall()
        #print(station_id_list)
        results = {}
        
        for i in station_id_list:

            station_id, = i
            postgres_select_query = """SELECT question, answers FROM question INNER JOIN answer ON question.question_id = answer.question_id WHERE question.station_id = {0} AND answer.patient_id = {1}""".format(station_id, patient_id)
            postgres_select_query2 = """SELECT station_name FROM station WHERE station_id = {0}""".format(station_id)
            cursor3.execute(postgres_select_query2)
            station_name, = cursor3.fetchall()[0]
            cursor2.execute(postgres_select_query)
            connection.commit()
            
            data = cursor2.fetchall()
            data = [dict(row) for row in data]

            num = 1
            for j in data:
                  #print(j)
                  j['num'] = num
                  num = num + 1

            results.update({station_name : data})
            
        print("Successful query of question table.")
        #print(results)

        #{'Registration': [
        #   {'question': 'Name', 'answers': 'ans', 'num': 1}, 
        #   {'question': 'Gender', 'answers': 'ans2', 'num': 2}, 
        #   {'question': 'Age', 'answers': 'ans3', 'num': 3}, 
        #   {'question': 'Birthday', 'answers': 'ans4', 'num': 4}
        #   ]
        # }

        return results
  
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while getting question table and converting to JSON.", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# delete the patient's data (id and answers) from the database
@app.route('/delete_patient', methods=["GET"])
def delete_patient(patient_id):
    try:
        connection = connect_db()
        cursor = connection.cursor()

        # Delete patient
        postgres_delete_patient_query = """DELETE FROM patient WHERE patient_id = {0}""".format(patient_id)
        cursor.execute(postgres_delete_patient_query)
        connection.commit()
        print ("patient deleted from patient table")
  
        # Delete answer
        postgres_delete_answer_query = """DELETE FROM answer WHERE patient_id = {0}""".format(patient_id)
        cursor.execute(postgres_delete_answer_query)
        connection.commit()
        print ("patient answers deleted from answer table")

    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while deleting patient", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

@app.route('/get_availability', methods=["GET"])
def get_station_availability():
    try:
        connection = connect_db()
        cursor = connection.cursor()
            
        postgres_select_query = """SELECT station_name, availability FROM station"""
        cursor.execute(postgres_select_query)
        connection.commit()

        results = cursor.fetchall()
        results = dict(results)
        
        print("Successful query of station table.")
        print(results)

        # {'Tobacco Questionnare': True, 
        # 'Anemia Questionnare': True, 
        # 'BMI (Underweight measurement)': True, 
        # 'Haemoglobin (Anemia measurement)': True, 
        # 'Post campaign survey': True, 
        # 'Registration': False}

        return results
      
    except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while getting question table and converting to JSON.", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")

# Use localhost for local database (with the default password set for your system). For now, I think we should
# continue using the postgres db on heroku so that everyone can perform queries on it. - Wei Kit
# This one i'm not v sure how to connect to a local db, so i've connected to another one i've deployed on heroku, can i get some help here?
def connect_db():
        connection = psycopg2.connect(user = "jhfdzctgeytrkt",
                            password = "6f0913d556bf6eee840e0e2ba8b4c0b3ef0331f6855852008be07eeb840cdb6f",
                            host = "ec2-35-173-94-156.compute-1.amazonaws.com",
                            port = "5432",
                            database = "dbpduk6f0fbp8q")
        return connection

# Create station table
def create_station():
      try:
            connection = connect_db()
            cursor = connection.cursor()

            create_stations_table_query = '''CREATE TABLE IF NOT EXISTS station
                  (station_id SERIAL PRIMARY KEY,
                  station_name TEXT UNIQUE,
                  availability BOOLEAN); '''
            cursor.execute(create_stations_table_query)
            connection.commit()
            print("Table station created successfully in PostgreSQL ")

      except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating station table", error)

      finally:
            #closing database connection.
            if(connection):
                  cursor.close()
                  connection.close()
                  #print("PostgreSQL connection is closed")

# Create patient table
def create_patient():
      try:
            connection = connect_db()
            cursor = connection.cursor()

            create_patients_table_query = '''CREATE TABLE IF NOT EXISTS patient
                  (patient_id SERIAL PRIMARY KEY,
                  status TEXT,
                  completed_station INTEGER[]); '''
            cursor.execute(create_patients_table_query)
            connection.commit()
            print("Table patient created successfully in PostgreSQL ")

      except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating patient table", error)

      finally:
            #closing database connection.
            if(connection):
                  cursor.close()
                  connection.close()
                  #print("PostgreSQL connection is closed")

# Create question table
def create_question():
      try:
            connection = connect_db()
            cursor = connection.cursor()

            create_questions_table_query = '''CREATE TABLE IF NOT EXISTS question
                  (question_id SERIAL PRIMARY KEY,
                  question TEXT,
                  station_id INTEGER,
                  type_id INTEGER); '''
            cursor.execute(create_questions_table_query)
            connection.commit()
            print("Table question created successfully in PostgreSQL ")

      except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating question table", error)

      finally:
            #closing database connection.
            if(connection):
                  cursor.close()
                  connection.close()
                  #print("PostgreSQL connection is closed")

# Create answer table
def create_answer():
      try:
            connection = connect_db()
            cursor = connection.cursor()

            create_answers_table_query = '''CREATE TABLE IF NOT EXISTS answer
                  (answer_id SERIAL PRIMARY KEY,
                  patient_id INTEGER,
                  answers TEXT,
                  question_id INTEGER,
                  station_id INTEGER); '''
            cursor.execute(create_answers_table_query)
            connection.commit()
            print("Table answer created successfully in PostgreSQL ")

      except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating answer table", error)

      finally:
            #closing database connection.
            if(connection):
                  cursor.close()
                  connection.close()
                  #print("PostgreSQL connection is closed")

# Create type table
def create_type():
      try:
            connection = connect_db()
            cursor = connection.cursor()

            create_type_table_query = '''CREATE TABLE IF NOT EXISTS type
                  (type_id SERIAL PRIMARY KEY,
                  type_info TEXT); '''
            cursor.execute(create_type_table_query)
            connection.commit()
            print("Table type created successfully in PostgreSQL ")

      except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating type table", error)

      finally:
            #closing database connection.
            if(connection):
                  cursor.close()
                  connection.close()
                  #print("PostgreSQL connection is closed")

# Create all the tables
def db_setup():
      create_station()
      create_patient()
      create_question()
      create_answer()
      create_type()

# Insert stations into station table
def insert_station(station_name):
      try:
            connection = connect_db()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO station (station_id, station_name, availability) VALUES (DEFAULT, %s, TRUE)"""
            record_to_insert = (station_name,)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into station table")
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to insert record into station table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Insert patients into patient table
def insert_patient(status, completed_station):
      try:
            connection = connect_db()
            cursor = connection.cursor()

            postgres_insert_query = """ INSERT INTO patient (patient_id, status, completed_station) 
                                    VALUES (DEFAULT, %s, %s)"""
            record_to_insert = (status, completed_station,)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into patient table")
      except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into patient table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Insert questions into question table
def insert_question(question, station_id, type_id):
      try:
            connection = connect_db()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO question (question_id, question, station_id, type_id) VALUES (DEFAULT, %s, %s, %s)"""
            record_to_insert = (question, station_id, type_id,)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into question table")
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to insert record into question table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Insert answers into answer table
def insert_answer(patient_id, answer, question_id, station_id):
      try:
            connection = connect_db()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO answer (answer_id, patient_id, answers, question_id, station_id) VALUES (DEFAULT, %s, %s, %s, %s)"""
            record_to_insert = (patient_id, answer, question_id, station_id,)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into answer table")
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to insert record into answer table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Insert types into type table
def insert_type(type_info):
      try:
            connection = connect_db()
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO type (type_id, type_info) VALUES (DEFAULT, %s)"""
            record_to_insert = (type_info,)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into type table")
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to insert record into type table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Update the completed stations in patient table
def update_completed(patient_id, station_name):
      try:
            connection = connect_db()
            cursor = connection.cursor()

            postgres_select_query = """ SELECT completed_station FROM patient WHERE patient_id = %s"""
            record_to_select = (patient_id,)
            cursor.execute(postgres_select_query, record_to_select)
            completed = cursor.fetchone()[0]

            postgres_select_query = """ SELECT station_id FROM station WHERE station_name = %s"""
            record_to_select = (station_name,)
            cursor.execute(postgres_select_query, record_to_select)
            station_id = cursor.fetchone()[0]

            completed.append(station_id)

            postgres_update_query = """ UPDATE patient SET completed_station = %s WHERE patient_id = %s"""
            record_to_update = (completed, patient_id,)
            cursor.execute(postgres_update_query, record_to_update)
            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into patient table")

      except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into patient table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Read the questions from excel file
def read_questions(file):
      questions = []
      with open(file) as csvfile:
            file_reader = csv.reader(csvfile)
            for question in file_reader:
                  questions.append(question[0])
      return questions

# I'm not sure how to handle this too, I guess we have to standardize a format for the excel questions - Rollie
# Insert questions from excel file into question table (I'm not v sure what to insert for the type, do we manually insert since there's not really a pattern?)
def save_questions(file):
      questions = read_questions(file)
      station_id = 0
      type_id = 0
      for q in questions:
            if (q == "Registration"):
                  station_id = 1
                  continue
            elif (q == "Tobacco Questionnare"):
                  station_id = 2
                  continue
            elif (q == "Anemia Questionnare"):
                  station_id = 3
                  continue
            elif (q == "BMI (Underweight measurement)"):
                  station_id = 4
                  continue
            elif (q == "Haemoglobin (Anemia measurement)"):
                  station_id = 5
                  continue
            elif (q == "Post campaign survey"):
                  station_id = 6
                  continue
            insert_question(q, station_id, type_id)
      print("all questions added")

# Get the questions and type from each station (I've printed the station name, questions, and types in list form but I'm not sure how to return it in the format needed)
def get_questions(station_name):
      try:
            connection = connect_db()
            cursor = connection.cursor()

            postgres_select_query = """ SELECT station_id FROM station WHERE station_name = %s"""
            record_to_select = (station_name,)
            cursor.execute(postgres_select_query, record_to_select)
            connection.commit()
            station_id = cursor.fetchall()
            print(station_name)

            if (not station_id is None):
                  postgres_select_query = """ SELECT question FROM question WHERE station_id = %s"""
                  cursor.execute(postgres_select_query, station_id)
                  connection.commit()
                  questions = cursor.fetchall()
                  questions = [i[0] for i in questions]
                  print(questions)

                  postgres_select_query = """ SELECT type_info FROM type INNER JOIN question ON question.type_id = type.type_id WHERE question.station_id = %s"""
                  cursor.execute(postgres_select_query, station_id)
                  connection.commit()
                  types = cursor.fetchall()
                  types = [i[0] for i in types]
                  print(types)
            
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to select from question table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Get answers from a patient from a particular station (also printed in list form)
def get_answers(patient_id, station_id):
      try:
            connection = connect_db()
            cursor = connection.cursor()
            postgres_select_query = """ SELECT answers FROM answer WHERE patient_id = %s AND station_id = %s"""
            record_to_select = (patient_id, station_id,)
            cursor.execute(postgres_select_query, record_to_select)
            connection.commit()
            answers = cursor.fetchall()
            answers = [i[0] for i in answers]
            print(answers)
      except (Exception, psycopg2.Error) as error:
            if(connection):
                print("Failed to select from question table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# set availability of station to false
def set_availability_false(station_name):
      try:
            connection = connect_db()
            cursor = connection.cursor()

            postgres_select_query = """ UPDATE station SET availability = %s WHERE station_name = %s"""
            record_to_select = (False, station_name,)
            cursor.execute(postgres_select_query, record_to_select)
            connection.commit()
            print("Availability set to false")

      except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into station table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# set availability of station to true
def set_availability_true(station_name):
      try:
            connection = connect_db()
            cursor = connection.cursor()

            postgres_select_query = """ UPDATE station SET availability = %s WHERE station_name = %s"""
            record_to_select = (True, station_name,)
            cursor.execute(postgres_select_query, record_to_select)
            connection.commit()
            print("Availability set to true")

      except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into station table", error)
      finally:
            if(connection):
                cursor.close()
                connection.close()
                #print("PostgreSQL connection is closed")

# Testing if info is inserted successfully
def insert_stuff_test():
      insert_type("text")
      insert_type("radio")
      insert_patient("busy", [])
      insert_patient("busy", [])
      insert_answer(1, "answer", 1, 1)
      insert_answer(1, "answer", 2, 1)

# Insert all the stations
def insert_stations():
      insert_station("Registration")
      insert_station("Tobacco Questionnare")
      insert_station("Anemia Questionnare")
      insert_station("BMI (Underweight measurement)")
      insert_station("Haemoglobin (Anemia measurement)")
      insert_station("Post campaign survey")

#def main():
      #db_setup()
      #insert_stations()
      #save_questions("question.csv")
      #insert_stuff_test()
      #get_questions("Registration")
      #get_answers(1,1)
      #update_completed(1, "registration")
      #set_availability_false("Registration")
      #get_station_availability()

#if __name__ == '__main__':    
      #main()

if __name__ == '__main__':
      app.run(debug=True)