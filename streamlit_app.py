import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My MOM's new healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 and blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build your Own Fruit Smoothie 🥝 🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
   # python package library requests
    # streamlit.text(fruityvice_response.json())
    # streamlit.write('User entered',fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # json version of the response converted to normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # output return
    return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice!')
try:
  # fruit choice
  fruit_choice = streamlit.text_input('What fruit would you like to know about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
    

# snowflake connection
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
# my_data_rows = my_cur.fetchall()

streamlit.header("View Our Fruit List - Add Your Favorites!")
# snowflake related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()
#  Add a button to load the fruit
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)

# new fruit addition option 
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      # inserting a new fruit to db
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+ new_fruit +"')")
      return "Thanks for adding " + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
#  Add a button to load the fruit
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)

# don't run anything past here while we troubleshoot
# streamlit.stop()
