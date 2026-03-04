
#CREATE CONNECTION WITH THE SQL SERVER
#DISPLAY THE RESULT IF THE CONNECTION IS DONE SUCCESSFULLY OR DISPLAY THE ERROR
def create_connection():
    
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="logistics"
        )
        if connection.is_connected():
            print("Successfully connected to MySQL")
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None
    
#FETCH THE RECORDS FOR THE QUERY
def res_fn(connection,query):
     #This function is to fetch the results from the query
     import pandas as pd
     cursor=connection.cursor()
     # Execute a SELECT statement

     cursor.execute(query)
     # Fetch all results from the executed query
     results=cursor.fetchall()
     
     #COPY THE RESULTS TO A DATAFRAME

     df=pd.DataFrame(results,columns=[i[0] for i in cursor.description])        
     cursor.close()
     return results,df
