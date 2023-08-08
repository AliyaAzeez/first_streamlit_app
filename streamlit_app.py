import streamlit
import pandas

streamlit.title("My MOM's new healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 and blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build your Own Fruit Smoothie 🥝 🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
