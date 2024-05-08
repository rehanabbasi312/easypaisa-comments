
from db import ReturnDatabaseObject
import pandas as pd

# PUSH DATA TO BUSINESS TABLE IN DATABASE
def insertDataIntoUserEmailTable(guid, sender_email, body, current_datetime_pkt):
    connection = ReturnDatabaseObject()
    # Define the SQL INSERT query
    sql_insert = """
    INSERT INTO userEmail (guid, email, emailbody, DateTime)
    VALUES (?, ?, ?, ?)
    """

    # Define the parameters to be inserted
    param_values = (guid, sender_email, body, current_datetime_pkt)

    # Create a cursor object
    cursor = connection.cursor()

    try:
        # Execute the INSERT query with parameters
        cursor.execute(sql_insert, param_values)
        # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        # Rollback the transaction if an error occurs
        connection.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

def insertDataIntoUserComplainTable(userguid, emailmessage, messageresponse, identifiedNumber, identifiedIssue, identifiedAmount, identifiedTransactionId, identifiedTransactionTime):
    connection = ReturnDatabaseObject()
    # Define the SQL INSERT query
    sql_insert = """
    INSERT INTO userComplain (userguid, emailmessage, messageresponse, identifiedNumber, identifiedIssue, identifiedAmount, identifiedTransactionId, identifiedTransactionTime)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Define the parameters to be inserted
    param_values = (userguid, emailmessage, messageresponse, identifiedNumber, identifiedIssue, identifiedAmount, identifiedTransactionId, identifiedTransactionTime)

    # Create a cursor object
    cursor = connection.cursor()

    try:
        # Execute the INSERT query with parameters
        cursor.execute(sql_insert, param_values)
        # Commit the transaction
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        # Rollback the transaction if an error occurs
        connection.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

def getDataFromUserEmail(mydb):
    qry="SELECT * FROM userEmail"
    df=pd.read_sql_query(qry,mydb)
    return df
    
def getDataFromUserComplain(mydb, guid):
    qry = "SELECT * FROM userComplain WHERE userguid = ?"
    df = pd.read_sql_query(qry, mydb, params=(guid,))
    return df

def updateDataToUserComplain(guid, identifiedNumber, identifiedAmount, identifiedTransactionId, identifiedTransactionTime):
    # Define the SQL UPDATE query
    mydb = ReturnDatabaseObject()
    sql_update = """
    UPDATE userComplain
    SET identifiedNumber = ?,
        identifiedAmount = ?,
        identifiedTransactionId = ?,
        identifiedTransactionTime = ?
    WHERE userguid = ?
    """

    # Define the parameters to be updated
    param_values = (identifiedNumber, identifiedAmount, identifiedTransactionId, identifiedTransactionTime, guid)

    # Create a cursor object
    cursor = mydb.cursor()

    try:
        # Execute the UPDATE query with parameters
        cursor.execute(sql_update, param_values)
        # Commit the transaction
        mydb.commit()
        print("Data updated successfully.")
    except Exception as e:
        # Rollback the transaction if an error occurs
        mydb.rollback()
        print(f"Error updating data: {e}")
    finally:
        cursor.close()

