#IMPORT THE REQUIRED LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from connection import create_connection
from connection import res_fn

#Read the  data from route sql table
conn=create_connection()
query="select * from routes"
results,route_df=res_fn(conn,query)



#FIND THE AVERAGE DELIVERY TIME PER ROUTE

def aver_del_time_per_route():
   conn=create_connection()
   query="""select r.route_id,r.origin,r.destination,avg(datediff(s.delivery_date,s.order_date))  as Average_Delivery_Days_Per_Route
   from routes r join shipments s 
   on r.origin =s.origin and r.destination=s.destination 
   where s.order_date is not null and 
         s.delivery_date is not null and s.status='Delivered'
   group by r.route_id,r.origin,r.destination
   order by Average_Delivery_Days_Per_Route desc"""
   results,df=res_fn(conn,query)
   
   return df
   

#BOX PLOT FOR THE AVERAGE DELIVERY TIME
def box_plot1():
    # Create a figure and axis explicitly
    fig, ax = plt.subplots(figsize=(6,6))
    sns.boxplot(y=route_df["avg_time_hours"], color="lightgreen", ax=ax)
    ax.set_ylabel("Average Delivery Time (hours)")
    return fig   # ✅ return the figure object

#HIST PLOT TO SHOW THE AVERAGE DELIVERY TIME DISTRIBUTION 
def hist_plot1():
    fig, ax = plt.subplots(figsize=(8,6))
    sns.histplot(route_df["avg_time_hours"], bins=20, kde=True, color="skyblue", ax=ax)

    # Custom ticks every 2 hours
    ax.set_xticks(np.arange(0, route_df["avg_time_hours"].max()+2, 2))
    ax.set_xlabel("Average Delivery Time (Hours)")
    ax.set_ylabel("Number of Routes per bin")
    
    return fig

#TOP 10 DELAYED ROUTES


def top10_delayed_plot():
   conn=create_connection()
   query="""select r.route_id,r.origin,r.destination,avg(datediff(s.delivery_date,s.order_date))  as Average_Delivery_Days_Per_Route
   from routes r join shipments s 
   on r.origin =s.origin and r.destination=s.destination 
   where s.order_date is not null and 
         s.delivery_date is not null and s.status='Delivered'
   group by r.route_id,r.origin,r.destination
   order by Average_Delivery_Days_Per_Route desc"""
   results,df=res_fn(conn,query)
   df1=df.head(10)
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df1,x="route_id",y="Average_Delivery_Days_Per_Route",color="Green")
   ax.set_title("TOP 10 Routes With Long Delivery Times")
   ax.set_xlabel("Route ids")
   ax.set_ylabel("Delivery Times")
   plt.xticks(rotation=45)
   return fig
#PLOT TO DISPLAY THE DELIVERY TIME Vs DISTANCE
def del_time_dist():

   conn=create_connection()
   query="""select r.route_id,r.origin,r.destination,r.distance_km,avg(datediff(s.delivery_date,s.order_date))  as Average_Delivery_Days_Per_Route
   from routes r join shipments s 
   on r.origin =s.origin and r.destination=s.destination 
   where s.order_date is not null and 
         s.delivery_date is not null and s.status='Delivered'
   group by r.route_id,r.origin,r.destination,r.distance_km
   order by Average_Delivery_Days_Per_Route desc"""
   results,df=res_fn(conn,query)
   #df1=df.head(10)
   fig,ax=plt.subplots(figsize=(8,6))
   sns.scatterplot(data=df,x="distance_km",y="Average_Delivery_Days_Per_Route",color="Green")
   ax.set_title("Distance Vs Average_Delivery_Days_Per_Route")
   ax.set_xlabel("Distance of the Route in km")
   ax.set_ylabel("Average_Delivery_Days_Per_Route")
   plt.xticks(rotation=45)
   return fig,df
 
#PLOT TO DISPLAY THE UNDER PERFORMING ROUTES
def under_performing_routes():
   conn=create_connection()
   query="""
    select r.route_id,r.distance_km as Distance,count(s.shipment_id) As Shipment_count,round(count(s.shipment_id)/r.distance_km,4) as Efficiency 
    from logistics.routes r join logistics.shipments s 
    on s.origin = r.origin and s.destination =r.destination
    group by r.route_id,r.distance_km
    order by Efficiency  asc

    """
   results,df=res_fn(conn,query)
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df.head(20),x="route_id",y="Efficiency")
   ax.set_title("Top 20 Under Performing Routes Relative To Distance")
   ax.set_xlabel("Route-id")
   ax.set_ylabel("Efficiency(Shipment count/Distance)")
   plt.xticks(rotation=45)
   return  fig,df

#COURIER PERFORMANCE
def courier_performance():
   conn=create_connection()
   query="select  courier_id,count(shipment_id) from logistics.shipments group by courier_id order by count(shipment_id) desc"
   results,df=res_fn(conn,query)
   max_shipment_courier_id_top10=df.head(20)
   
   
   max_shipment_courier_id_top10.columns=["Courier_id","Shipment_count"]
   print("The Top 10 courier ids with max shipments ")
   print(max_shipment_courier_id_top10)

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=max_shipment_courier_id_top10,x="Courier_id",y="Shipment_count",color="skyblue")
   ax.set_title("Top 10 Courier ids with Max shipments")
   ax.set_xlabel("Courier ids")
   ax.set_ylabel("Number of shipments")
   plt.xticks(rotation=45)
   return fig,df
#ON TIME DELIVERY
def ontime_delivery():
   conn=create_connection()
   query="""  
   WITH ontime_status AS (
    SELECT 
        r.route_id,
        r.origin,
        r.destination,
        r.avg_time_hours AS Average_delivery_hours,
        TIMESTAMPDIFF(
            HOUR,
            o.timestamp,
            d.timestamp
        ) AS Actual_delivery_hours,
        CASE 
            WHEN TIMESTAMPDIFF(HOUR, o.timestamp, d.timestamp) <= r.avg_time_hours 
            THEN 'on-time' 
            ELSE 'delayed'  
        END AS Delivery_status
    FROM logistics.routes r
    JOIN logistics.shipments s 
        ON r.origin = s.origin 
       AND r.destination = s.destination
    JOIN logistics.shipment_tracking o 
        ON s.shipment_id = o.shipment_id AND o.status = 'Order Placed'
    JOIN logistics.shipment_tracking d 
        ON s.shipment_id = d.shipment_id AND d.status = 'Delivered'
    WHERE s.status = 'Delivered'
)
SELECT 
    route_id,
    origin,
    destination,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN Delivery_status = 'on-time' THEN 1 ELSE 0 END) AS on_time_shipments,
    ROUND(
        (SUM(CASE WHEN Delivery_status = 'on-time' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
        2
    ) AS on_time_percentage
FROM ontime_status
GROUP BY route_id, origin, destination
ORDER BY on_time_percentage DESC;
"""
   results,df=res_fn(conn,query)
     
   return df

#COURIER RATING Vs DELIVERY TIME
def courier_rating_del_time():
   conn=create_connection()
   query="""select s.courier_id,avg(datediff(s.delivery_date,s.order_date)) as Avg_delivery_time,c.rating 
     from logistics.shipments s join logistics.courier_staff c 
     on s.courier_id=c.courier_id 
     group by s.courier_id,c.rating 
     order by c.rating  desc;"""
   results,df=res_fn(conn,query)
   return df

#TOP 10 COURIER RATINGS
def courier_rating():
   conn=create_connection()
   query="select * from courier_staff order by rating desc"
   results,courier_staff=res_fn(conn,query)

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=courier_staff.head(30),x="courier_id",y="rating",color="red")
   ax.set_title("Top 30 Courier ids with Good Rating")
   ax.set_xlabel("Courier_ids")
   ax.set_ylabel("Rating")
   plt.xticks(rotation=45)
   return fig

#TOTAL COST PER SHIPMENT
def costs_1():
   conn=create_connection()
   query=""" 
select c.shipment_id, round(c.fuel_cost+c.labor_cost+c.misc_cost,2) as Total_cost,r.distance_km,s.weight
from logistics.shipments s join logistics.costs c 
on s.shipment_id =c.shipment_id
join logistics.routes r 
on s.origin=r.origin and 
s.destination= r.destination
order by Total_cost desc;
"""
   results,df=res_fn(conn,query)
   return df
   
#TOTAL COST PER ROUTE
def cost_per_route():
   conn=create_connection()
   query="""
      SELECT 
    r.route_id,
    SUM(c.fuel_cost) AS total_fuel_cost,
    SUM(c.labor_cost) AS total_labor_cost,
    SUM(c.misc_cost) AS total_misc_cost,
    (SUM(c.fuel_cost) + SUM(c.labor_cost) + SUM(c.misc_cost)) AS total_cost_per_route
    FROM 
    routes r
    JOIN 
    shipments s
    ON r.origin = s.origin
    AND r.destination = s.destination
    JOIN 
    costs c
    ON s.shipment_id = c.shipment_id
    WHERE 
    c.fuel_cost IS NOT NULL
    AND c.labor_cost IS NOT NULL
    AND c.misc_cost IS NOT NULL
    GROUP BY 
    r.route_id
    ORDER BY 
    r.route_id;
"""

   results,df=res_fn(conn,query)
   
   print("Total Cost Per Route:")
   df1=df[['route_id','total_cost_per_route']].sort_values(by='total_cost_per_route',ascending=False)
   df1=df1.reset_index(drop=True)
   print(df1)
   top_20_df=df.sort_values(by="total_cost_per_route",ascending=False).head(20)
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=top_20_df,x="route_id",y="total_cost_per_route",color="red")
   ax.set_title("Top 20 most expensive route ids ")
   ax.set_xlabel("Route_ids")
   ax.set_ylabel("Total Cost Per Route")
   plt.xticks(rotation=45)
   
   return fig,df1
#FUEL AND LABOR COSTS CONTRIBUTION TO THE TOTAL COST
def fuel_labor_contribution():
   conn=create_connection()
   query="""
SELECT 

    shipment_id,
    (fuel_cost + labor_cost + misc_cost) AS total_cost,
    fuel_cost * 100.0 / (fuel_cost + labor_cost + misc_cost) AS fuel_cost_percentage_contribution,
    labor_cost * 100.0 / (fuel_cost + labor_cost + misc_cost) AS labor_cost_percentage_contribution,
    misc_cost * 100.0 / (fuel_cost + labor_cost + misc_cost) AS misc_cost_percentage_contribution
FROM 
    costs;

"""
   results,df=res_fn(conn,query)
   df=df.sort_values(by="total_cost",ascending=False)
  
   df = df.set_index('shipment_id')
   
   return df


#Top 20 most expensive shipment ids
def costs_2():
   costs_df=pd.read_csv(r"D:\VS_CODE\Logistics\costs.csv")
    
   costs_df["Total_cost"]=costs_df["fuel_cost"]+costs_df["labor_cost"]+costs_df["misc_cost"]

   
   costs_df_top20=costs_df.sort_values(by="Total_cost",ascending=False).head(20).reset_index()
  
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=costs_df_top20,x="shipment_id",y="Total_cost",color="red")
   ax.set_title("Top 20 most expensive shipment ids ")
   ax.set_xlabel("Shipment_ids")
   ax.set_ylabel("Total Cost")
   plt.xticks(rotation=45)
   return fig

#Cancellation rate by origin
def cancellation_analysis1():
   conn=create_connection()
   query="""

    SELECT 
    origin,
    (SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) / COUNT(shipment_id) AS cancellation_rate_by_origin
    FROM 
    logistics.shipments
    GROUP BY 
    origin
    ORDER BY 
    cancellation_rate_by_origin DESC;


    """
   results,df=res_fn(conn,query)
   df1=df.sort_values(by="cancellation_rate_by_origin",ascending=False).head(20).reset_index()
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df1,x="origin",y="cancellation_rate_by_origin",color="green")
   ax.set_title("Top 20 Origins with Highest Cancellation Rate ")
   ax.set_xlabel("Origin")
   ax.set_ylabel("Cancellation_rate_by_origin")
   plt.xticks(rotation=45)
   return fig,df

#Cancellation_rate_by_courier_id
def cancellation_analysis2():
   conn=create_connection()
   query="""

    SELECT 
    courier_id,
    (SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) / COUNT(shipment_id) AS cancellation_rate_by_courier_id
    FROM 
    logistics.shipments
    GROUP BY 
    courier_id
    ORDER BY 
    cancellation_rate_by_courier_id DESC;

    """
   results,df=res_fn(conn,query)
   df1=df.sort_values(by="cancellation_rate_by_courier_id",ascending=False).head(20).reset_index()
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df1,x="courier_id",y="cancellation_rate_by_courier_id",color="green")
   ax.set_title("Top 20 Courier ids with Highest Cancellation Rate ")
   ax.set_xlabel("Courier_ids")
   ax.set_ylabel("Cancellation_rate_by_courier_ids")
   plt.xticks(rotation=45)
   return fig,df

#TIME TO CANCELLATION ANALYSIS
def cancellation_analysis3():
   
  conn=create_connection()
  query="""
 WITH latest_orders AS (
    SELECT 
        shipment_id,
        MAX(timestamp) AS order_time
    FROM logistics.shipment_tracking
    WHERE status = 'Order Placed'
    GROUP BY shipment_id
),
cancelled AS (
    SELECT 
        shipment_id,
        MIN(timestamp) AS cancel_time
    FROM logistics.shipment_tracking
    WHERE status = 'Cancelled'
    GROUP BY shipment_id
)
-- Step 2: Join them together and order by cancellation time
SELECT 
    c.shipment_id,
    TIMESTAMPDIFF(HOUR, o.order_time, c.cancel_time) AS time_to_cancellation_hours
FROM latest_orders o
JOIN cancelled c 
  ON o.shipment_id = c.shipment_id
WHERE c.shipment_id IN (
    SELECT shipment_id 
    FROM logistics.shipments 
    WHERE status = 'Cancelled'
)
ORDER BY c.cancel_time desc;   -- sort by cancellation time, but don’t display it

  """

  results,df=res_fn(conn,query)
  return df

#Warehouse capacity comparison
def warehouse1():
   conn=create_connection()
   query="""
select  warehouse_id,capacity from warehouses order by capacity desc

"""
   results,df=res_fn(conn,query)
   df1=df.sort_values(by="capacity",ascending=False).head(20).reset_index()
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df1,x="warehouse_id",y="capacity",color="blue")
   ax.set_title("Top 20 Warehouses with Largest Capacity ")
   ax.set_xlabel("Warehouse_id")
   ax.set_ylabel("Capacity")
   plt.xticks(rotation=45)
   return fig,df

#High traffic warehouse cities
def warehouse2():
   conn=create_connection()
   query="""

SELECT 
    w.warehouse_id,
    w.city,
    s.shipment_count
FROM logistics.warehouses w
JOIN (
    SELECT 
        origin AS city,
        COUNT(shipment_id) AS shipment_count
    FROM logistics.shipments
    GROUP BY origin
    ORDER BY shipment_count DESC
    LIMIT 20
) s
ON w.city = s.city
order by s.shipment_count desc limit 20 ;

"""
   results,df=res_fn(conn,query)
   
   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=df,x="city",y="shipment_count",color="blue")
   ax.set_title("Top 20 Warehouse Cities with High Traffic ")
   ax.set_xlabel("City")
   ax.set_ylabel("Shipment Count")
   plt.xticks(rotation=45)
   return fig,df
