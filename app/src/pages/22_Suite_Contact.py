import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests 

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Suite Contact')

st.write('\n\n')
st.title("Katherine Ahn")
st.markdown(
    """
    Email: ahn.ka@northeastern.edu
    \n Katherine Ahn is a rising fourth year Biology and Math major with minors in Data Science and 
    Global Health at Northeastern University. An aspiring Bioinformatician, Katherine is pursuing a 
    Masters in the field following graduation. Katherine has always been greatly interested in the 
    healthcare sector, and her education at Northeastern has provided her with the tools to look at 
    it from a lens she never considered – through a data filled lens.
    """
)
st.write('\n\n')
st.title("Anoushka Abroal")
st.write()
st.markdown(
    """
    Email: abroal.a@northeastern.edu
    \n Passionate and highly motivated Northeastern honors college student interested in research 
    opportunities to collaborate on real world challenges using AI, machine learning, and data science. 
    Experienced at working on individual research projects as well as team based initiatives. Detail-oriented 
    and project management-focused about completing my projects on time. Self-driven person who enjoys solving 
    technically challenging problems and researching new approaches to traditional solutions. Eager to take 
    on new challenges and enjoys collaborating with others. Focused on how technology can be leveraged for 
    better healthcare research outcomes. Held leadership roles in school and external clubs. Volunteered with 
    technical teams at the American Diabetes Association. Strong communication and task prioritization skills.
    """
)

st.write('\n\n')
st.title("Arthur Huang")
st.write()
st.markdown(
    """
    Email: huang.arth@northeastern.edu
    \n Arthur Huang is a 18 year old male computer science major with an electrical engineering minor at 
    Northeastern University. He is a very adventurous and team oriented individual who is eager to embark 
    on new projects and opportunites regarding software development and artificial intelligence. In his free 
    time, he enjoys golfing, skiing, and cooking.
    """
)

st.write('\n\n')
st.title("Shiven Ajwaliya")
st.write()
st.markdown(
    """
    Email: ajwaliya.s@northeastern.edu
    \n Hi, my name is Shiven Ajwaliya, a CS student at Northeastern University who loves learning new 
    things and traveling. I’m passionate about building meaningful tech products, exploring different 
    cultures, and discovering new places through local food and history.
    """
)

#st.write('\n\n')
st.title("Names of Ngos")

API_URL = "http://web-api:4000/ngo/ngos"

response = requests.get(API_URL)
ngos = response.json()

st.write("Names of Ngos")

for item in ngos:
    st.write(item["Name"])