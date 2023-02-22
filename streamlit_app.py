import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 avacardo toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Apple'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruity_vice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  a= pandas.json_normalize(fruityvice_response.json())
  return a

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select the fruit for information")
  else:
    back_from_function= get_fruity_vice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#streamlit.write('The user entered ', fruit_choice)

#import requests

#streamlit.text(fruityvice_response.json())

#streamlit.stop()

#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contain:")
def get_fruit_load_list():
  with  my_cnx.cursor() as  my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row=get_fruit_load_list()
  streamlit.dataframe(my_data_row)
  
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as  my_cur:
    my_cur.execute("insert into fruit_load_list values('from streamlit')")
    return "Thanks for adding" + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('add fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function =insert_row_snowflake(new_fruit)
  streamlit.text(back_from_function)
  

    

#streamlit.dataframe(my_data_row)

#fruit_choice = streamlit.text_input('What fruit would you like information about?')
#streamlit.write('The user entered ', fruit_choice)

#my_cur.execute("insert into fruit_load_list values('from streamlit')")
