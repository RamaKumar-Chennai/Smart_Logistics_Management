
from connection import create_connection
from connection import res_fn
import streamlit as st


#SHIPMENT SEARCH AND FILTERING
#SEARCH BY FILTER ID
def shipment_id_textbox():
    shipment_id=st.text_input(label="Enter the shipment id here")
    if shipment_id:
      
      conn=create_connection()
      
      query = f"SELECT * FROM shipments WHERE shipment_id = '{shipment_id}'"

      results,df1=res_fn(conn,query)
      if not df1.empty:
        st.success(f"The details for the shipment id:{shipment_id}")
        st.dataframe(df1)

        st.success(f"Further details for the shipment id:{shipment_id}")
        conn=create_connection()
      
        query = f"SELECT * FROM shipment_tracking WHERE shipment_id = '{shipment_id}'"

        results,df1=res_fn(conn,query)
        st.dataframe(df1)
      else:
         st.error(f"There are no shipment records for the shipment id:{shipment_id} ")
      
      
      
#GET THE UNIQUE STATUS OF THE SHIPMENT RECORDS
def status():
  conn=create_connection()
  query="select distinct status from shipments"
  cursor=conn.cursor()
  cursor.execute(query)
  results=cursor.fetchall()
  print("the resulls for unique status are",results)
  #the resulls for unique status are [('Cancelled',), ('Delivered',), ('In Transit',), ('Pending',)]

  unique_status= [i[0] for i in results]
  cursor.close()
  return unique_status

#FETCH THE SHIPMENT RECORDS FOR THE CORRESPONDING STATUS
def status_record(status):
    conn=create_connection()
    cursor=conn.cursor()
    query=f"select * from shipments where status='{status}'"
    results,df=res_fn(conn,query)
    return df

#FETCH THE UNIQUE ORIGIN CITIES
def origin():
   conn=create_connection()
   cursor=conn.cursor()
   query="select distinct origin from shipments"
   cursor.execute(query)
   results=cursor.fetchall()
   unique_origin=[i[0] for i in results]
   cursor.close()
   return unique_origin

#FETCH THE UNIQUE DESTINATION CITIES
def dest():
   conn=create_connection()
   cursor=conn.cursor()
   query="select distinct destination from shipments"
   cursor.execute(query)
   results=cursor.fetchall()
   unique_dest=[i[0] for i in results]
   cursor.close()
   return unique_dest

#FETCH THE SHIPMENT RECORDS FOR THE CORRESPONDING ORIGIN AND DESTINATION
def origin_dest(origin,dest):
    conn=create_connection()
    cursor=conn.cursor()
    query=f"select * from shipments where origin='{origin}' and destination='{dest}'"
    results,df=res_fn(conn,query)
    return df

#FETCH THE SHIPMENT RECORDS IN THE PARTICULAR TIME INTERVAL
def date_interval(sub3_choice,interval):
   conn=create_connection()
   #"Order date",
   if sub3_choice=="Order date":
      col="order_date"
   elif sub3_choice=="Delivery date":
      col="delivery_date"
   if interval =="Last Week":
     n=7
     unit="DAY"
   elif interval =="Last Month":
      n=1
      unit="MONTH"
   elif interval == "Last Quarter":
      n=3
      unit="MONTH"
   elif interval == "Last 6 months":
      n=6
      unit="MONTH"
   elif interval == "Last Year":
      n=1
      unit="YEAR"
  
   query=f"SELECT * FROM shipments WHERE {col} >= CURDATE() - INTERVAL {n} {unit} order by {col} desc"
   
   results,df=res_fn(conn,query)
   return df

#FETCH THE SHIPMENT RECORDS IN THE CUSTOM DATE RANGE
def custom_date(sub3_choice,start_dt,end_dt):
   print("start dt is ",start_dt)
   print("end dt is ",end_dt)
   if sub3_choice=="Order date":
      col="order_date"
   elif sub3_choice=="Delivery date":
      col="delivery_date"
   query=f"SELECT * FROM shipments WHERE {col} between '{start_dt}' and '{end_dt}' order by {col} desc"
   conn=create_connection()
   results,df=res_fn(conn,query)
   return df

#FETCH THE SHIPMENT RECORDS FOR COURIER ID
def courier_id_textbox():
    courier_id=st.text_input(label="Enter the courier id here")
    if courier_id:
      
      conn=create_connection()
      
      query = f"SELECT * FROM shipments WHERE courier_id = '{courier_id}'"

      results,df1=res_fn(conn,query)
      if not df1.empty:
         st.success(f"The Shipment details for the courier id: {courier_id}")
         st.dataframe(df1)
      else:
         st.error(f"There are no shipment records for this courier id: {courier_id}")


#KPI FILTERING
#TOTAL SHIPMENTS COUNT
def total_shipments():
   conn=create_connection()
   query="Select count(*) from shipments"
   cursor=conn.cursor()
   cursor.execute(query)
   results=cursor.fetchall()
   cursor.close()
   return results
#DELIVERED SHIPMENTS COUNT
def delivered_shipments():
   conn=create_connection()
   query="SELECT (SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS delivered_percentage FROM shipments"
   cursor=conn.cursor()
   cursor.execute(query)
   results=cursor.fetchall()
   cursor.close()
   return results

#CANCELLED SHIPMENTS COUNT
def cancelled_shipments():
   conn=create_connection()
   query="SELECT (SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS cancelled_percentage FROM shipments"
   cursor=conn.cursor()
   cursor.execute(query)
   results=cursor.fetchall()
   cursor.close()
   return results

#Avg_delivery_days of the shippments
def aver_del_time():
   conn=create_connection()
   query="SELECT AVG(DATEDIFF(delivery_date, order_date)) AS avg_delivery_days FROM shipments"
   cursor=conn.cursor()
   cursor.execute(query)
   results=cursor.fetchall()
   cursor.close()
   return results

#TOTAL COST PER SHIPMENT
def total_cost1():
   conn=create_connection()
   query="select shipment_id,fuel_cost+labor_cost+misc_cost as total_cost from costs"
   results,df=res_fn(conn,query)
   print("the datafraem is ",df)
   print("type of dataframe is ",type(df))
   return df
#TOTAL COST OF ALL SHIPMENTS
def total_cost2():
   conn=create_connection()
   query="select sum(fuel_cost+labor_cost+misc_cost) as total_cost from costs"
   cursor=conn.cursor()
   cursor.execute(query)
   results=cursor.fetchall()
   cursor.close()
   return results
