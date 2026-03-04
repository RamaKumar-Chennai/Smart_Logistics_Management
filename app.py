
#IMPORT THE REQUIRED FUNCTIONS FROM connection.py,select_data.py,analytical_views.py

import streamlit as st
from connection import create_connection
from connection import  res_fn
from select_data import shipment_id_textbox
from select_data import status
from select_data import status_record
from select_data import  origin
from select_data import dest
from select_data import origin_dest
from select_data import date_interval
from select_data import custom_date
from select_data import courier_id_textbox

from select_data import total_shipments
from select_data import delivered_shipments
from select_data import cancelled_shipments
from select_data import aver_del_time
from select_data import total_cost1
from select_data import total_cost2



from analytical_views import box_plot1
from analytical_views import hist_plot1
from analytical_views import top10_delayed_plot
from analytical_views import del_time_dist
from analytical_views import under_performing_routes

from analytical_views import courier_performance
from analytical_views import courier_rating_del_time
from analytical_views import courier_rating
from analytical_views import ontime_delivery
from analytical_views import costs_1
from analytical_views import aver_del_time_per_route
from analytical_views import cost_per_route
from analytical_views import fuel_labor_contribution
from analytical_views import costs_2
from analytical_views import cancellation_analysis1
from analytical_views import cancellation_analysis2
from analytical_views import cancellation_analysis3
from analytical_views import warehouse1
from analytical_views import warehouse2

#DISPLAY THE TITLE IN THE STREAMLIT PAGE
st.markdown(
    """
    <h1 style='text-align: left; color: teal;'>
        Smart Logistics Management and Analytics Platform
    </h1>
    """,
    unsafe_allow_html=True
)


#SIDEBAR MAIN HEADINGS
main_choice=st.sidebar.radio("Choose your main option",["Shipment Search & Filtering","Operational KPIs","Analytical Views"],index=None)

#Shipment Search & Filtering
if main_choice=="Shipment Search & Filtering":
   sub1_choice=st.sidebar.radio("Choose your sub option",["Search by shipment_id","Filter by"],index=None)
# Search by shipment_id  
   if sub1_choice=="Search by shipment_id":
       shipment_id_textbox()
       
#Filter by Status,Origin / Destination,Date range,Courier
   elif sub1_choice == "Filter by":
           sub2_choice=st.sidebar.selectbox("Choose your Filter option",["Status","Origin / Destination","Date range","Courier"],index=None)
           if sub2_choice=="Status":
              unique_status=status()
              status=st.selectbox("Enter the delivery status here",unique_status,index=None)
              if status:
               df=status_record(status)
               st.dataframe(df)
           elif sub2_choice=="Origin / Destination":
              unique_origin=origin() 
              unique_dest=dest()
              origin_city=st.selectbox("Enter the origin here",unique_origin,index=None)
              dest_city=st.selectbox("Enter the destination here",unique_dest,index=None)
              if origin_city and dest_city:
                df=origin_dest(origin_city,dest_city)
                if not df.empty:
                 
                 st.success(f"✅ Shipments from {origin_city} to {dest_city} found!", icon="📦")
                 st.dataframe(df)
                else:
                   
                 st.error(f"❌ No shipments from {origin_city} to {dest_city} found!", icon="🚫")

           elif sub2_choice=="Date range":
               sub3_choice=st.radio("Choose your date option",["Order date","Delivery date"],index=None)
               if sub3_choice=="Order date":
                 interval=st.selectbox("Enter the interval",["Last Week","Last Month","Last Quarter","Last 6 months","Last Year","Custom Range"],index=None)
               elif sub3_choice=="Delivery date":
                 interval=st.selectbox("Enter the interval",["Last Week","Last Month","Last Quarter","Last 6 months","Last Year","Custom Range"],index=None)
                 
               if sub3_choice and interval and interval!="Custom Range":
                 df=date_interval(sub3_choice,interval)  
                 if sub3_choice=="Order date":
                    ord_del="SHIPMENT ORDERS"
                 elif sub3_choice=="Delivery date":
                    ord_del="SHIPMENT DELIVERIES"
                 if not df.empty:
                    
                   st.success(f"{ord_del} in the {interval} :")
                   st.write(df) 
                 else:
                    st.error(f"❌ No {ord_del} in the {interval} found!", icon="🚫")
               if sub3_choice and interval and interval=="Custom Range":
                 if sub3_choice=="Order date":
                    ord_del="SHIPMENT ORDERS"
                 elif sub3_choice=="Delivery date":
                    ord_del="SHIPMENT DELIVERIES"
                 start_dt=st.date_input("Start Date")
                 end_dt=st.date_input("End Date")
                 custom_button=st.button("Show the records in this date range")

                 if custom_button and start_dt and end_dt:
                    if start_dt<end_dt:
                        df=custom_date(sub3_choice,start_dt,end_dt)
                        st.success(f"{ord_del} in the {interval} :")
                        st.write(df)
                    else:
                       st.error("Enter the start date and end date correctly")
                 elif not custom_button and not start_dt and not end_dt:
                    st.error("Please choose the date values and click the button to view the records") 
                  
           elif sub2_choice=="Courier":
               courier_id_textbox()
             
# Operational KPIs 
# Total Shipments,Delivered Shipments %,Cancelled Shipments %,Average Delivery Time,Total Operational Cost       
elif main_choice=="Operational KPIs":
   kpi_choice=st.radio("Enter the option here",["Total Shipments","Delivered Shipments %","Cancelled Shipments %","Average Delivery Time","Total Operational Cost"],index=None)
   if kpi_choice=="Total Shipments":
      results=total_shipments()
      print("results ",results)
       #results  [(70000,)]
      st.success(f"The Total number of shipments: {results[0][0]}")
   elif kpi_choice=="Delivered Shipments %":
      results=delivered_shipments()
      print("results ",results)
      #results  [(Decimal('24.76571'),)]
      results=round(results[0][0],2)
      
      st.success(f"Delivered Shipments - {results} %")
   elif kpi_choice=="Cancelled Shipments %":
      results=cancelled_shipments()
      print("results ",results)
      #results  [(Decimal('25.04000'),)]
      results=round(results[0][0],2)
      st.success(f"Cancelled Shipments - {results} %")
   elif kpi_choice=="Average Delivery Time":

      results=aver_del_time()
      print("results ",results)
      #results  [(Decimal('3.9934'),)]
      results=round(results[0][0],2)
      st.success(f"Average Delivery time   -   {results} days ")
   elif kpi_choice=="Total Operational Cost":
      cost_choice=st.radio("Choose the cost option",["Per Shipment cost","Overall Operational Cost"],index=None)
      if cost_choice=="Per Shipment cost":
        df=total_cost1()
        st.success("Total Cost Per Shipment : ")
        st.dataframe(df)
   
      elif cost_choice=="Overall Operational Cost":
        results=total_cost2()
        print("results",results)
        #results [(11731097.389999827,)]
        results=results[0][0]
        
        
        results=f"{results:,.2f}"
        st.success(f"Overall Operational Cost : {results}")

       
#Analytical Views
#Delivery Performance Insights,Courier Performance,Cost Analytics,Cancellation Analysis,Warehouse Insights
elif main_choice=="Analytical Views":
   av1_choice=st.sidebar.radio("Enter your choice here",["Delivery Performance Insights","Courier Performance","Cost Analytics","Cancellation Analysis","Warehouse Insights"],index=None)
      
   if av1_choice=="Delivery Performance Insights":
#Average delivery time per route,Most delayed routes,Delivery time vs distance comparison,Under Performing Routes Relative To Distance
      av1_sub_choice=st.radio("Enter your choice here",["Average delivery time per route","Most delayed routes","Delivery time vs distance comparison","Under Performing Routes Relative To Distance"],index=None)
      if av1_sub_choice=="Average delivery time per route":
         df=aver_del_time_per_route()
         st.success("Average delivery time per route ")
         st.dataframe(df)
        

         st.header("Box plot for Average Delivery times across routes")
         fig1=box_plot1()
         st.pyplot(fig1)
         
         st.header("Distribution of Average Delivery Times Across Routes")
         fig2=hist_plot1()
         st.pyplot(fig2)


      elif av1_sub_choice=="Most delayed routes":
        
        fig3=top10_delayed_plot()
        st.pyplot(fig3)
      
      elif av1_sub_choice=="Delivery time vs distance comparison" :
         fig4,df=del_time_dist()
         st.success("Delivery time vs distance comparison ")
         st.dataframe(df)
         st.pyplot(fig4)
      elif av1_sub_choice=="Under Performing Routes Relative To Distance" :
         fig,df=under_performing_routes()
         st.success("Under Performing Routes Relative To Distance")
         st.dataframe(df)
         st.pyplot(fig)

   elif av1_choice=="Courier Performance":  
#Shipments handled per courier,On-time delivery %,Courier Rating Vs Delivery Time,Average rating comparison
       av2_sub_choice=st.radio("Enter your choice here",["Shipments handled per courier","On-time delivery %","Courier Rating Vs Delivery Time","Average rating comparison"],index=None)
       if av2_sub_choice=="Shipments handled per courier":
          fig,df= courier_performance()
          st.success("Shipments Handled Per Courier")
          st.dataframe(df)
          st.pyplot(fig)

       elif av2_sub_choice=="On-time delivery %":  
          df=ontime_delivery()
          st.success("On-time delivery %")
          st.dataframe(df)
       elif av2_sub_choice=="Courier Rating Vs Delivery Time":
          df=courier_rating_del_time()
          st.success("Courier Rating Vs Delivery Time")
          st.dataframe(df)
          st.info("There is no link between Courier Staff Rating and Delivery Time.The Delivery Time depends on the Distance between the Origin and Destination")

       elif av2_sub_choice=="Average rating comparison":

        fig=courier_rating()
        st.pyplot(fig)
   
   #Cost Analytics
   elif  av1_choice=="Cost Analytics":
   #Total cost per shipment,Cost per route,Fuel vs labor percentage contribution,High-cost shipments
      cost_analytics_subchoice=st.radio("Enter your choice here",["Total cost per shipment","Cost per route","Fuel vs labor percentage contribution","High-cost shipments"],index=None)
      if cost_analytics_subchoice=="Total cost per shipment":
         df=costs_1()
         st.success("Total Cost Per Shipment")
         st.dataframe(df)
         st.info("The Total Cost Per Shipment is directly proportional to  the Distance and not to the weight")
         
      elif cost_analytics_subchoice=="Cost per route":
        fig,df=cost_per_route()
        st.success("Total Cost Per Route")
        st.dataframe(df)
        st.pyplot(fig)
      elif cost_analytics_subchoice=="Fuel vs labor percentage contribution":
          df=fuel_labor_contribution()
          st.success("Fuel-labor-cost-percentage-contribution")
          st.dataframe(df)
      elif cost_analytics_subchoice=="High-cost shipments":
         fig=costs_2()
         st.success("High-Cost Shipments")
         st.pyplot(fig)
#Cancellation Analysis
   elif av1_choice=="Cancellation Analysis":
#Cancellation rate by origin","Cancellation rate by courier","Time-to-cancellation analysis
      av2_sub_choice=st.radio("Enter your choice here",["Cancellation rate by origin","Cancellation rate by courier","Time-to-cancellation analysis"],index=None)   
      if av2_sub_choice =="Cancellation rate by origin":
         fig,df=cancellation_analysis1()
         st.success("Cancellation rate by origin")
         st.dataframe(df)
         st.pyplot(fig)

      elif av2_sub_choice =="Cancellation rate by courier":
         fig,df=cancellation_analysis2()
         st.success("Cancellation rate by Courier")
         st.dataframe(df)
         st.pyplot(fig)


      elif av2_sub_choice =="Time-to-cancellation analysis":
         df=cancellation_analysis3()
         st.success("Time-to-cancellation analysis")
         st.dataframe(df)
        
#Warehouse Insights
   elif av1_choice=="Warehouse Insights":
#Warehouse capacity comparison,High-traffic warehouse cities
      av2_sub_choice=st.radio("Enter your choice here",["Warehouse capacity comparison","High-traffic warehouse cities"],index=None) 
      if av2_sub_choice=="Warehouse capacity comparison":
          fig,df=warehouse1()
          st.success("Warehouse capacity comparison")
          st.dataframe(df)
          st.pyplot(fig)

      elif av2_sub_choice=="High-traffic warehouse cities":
          fig,df=warehouse2()
          st.success("High-traffic warehouse cities")
          st.dataframe(df)
          st.pyplot(fig)

         




         



