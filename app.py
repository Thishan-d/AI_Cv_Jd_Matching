import Test6 as T6
import time
import os
from PIL import Image
import Similar
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from pandas._config.config import options
from wordcloud import WordCloud
from operator import index
import gensim.corpora as corpora
import gensim
import matplotlib.colors as mcolors
import nltk
nltk.download('popular')

#############################################
image = Image.open('Images//logo.png')
st.image(image, use_column_width=True)

st.title("Resume Matcher")
# Reading the CSV files prepared by the fileReader.py
Resumes = pd.read_csv('Resume_Data.csv')
Jobs = pd.read_csv('Job_Data.csv')


############################### JOB DESCRIPTION CODE ######################################
# Checking for Multiple Job Descriptions
# If more than one Job Descriptions are available, it asks user to select one as well.
if len(Jobs['Name']) <= 1:
    st.write(
        "There is only 1 Job Description present. It will be used to create scores.")
else:
    st.write("There are ", len(Jobs['Name']),
             "Job Descriptions available. Please select one.")


# Asking to Print the Job Desciption Names
if len(Jobs['Name']) > 1:
    index = [a for a in range(len(Jobs['Name']))]
    fig = go.Figure(data=[go.Table(header=dict(values=["Job Descreption Name"],  line_color='darkslategray', fill_color='lightblue'), cells=dict(
        values=[Jobs['Name']], line_color='darkslategray', fill_color='lightgray'))])
    fig.update_layout(width=700, height=400)
    st.write(fig)


# Asking to chose the Job Description
# index = st.slider("Which JD to select ? : ", 0,
#                   len(Jobs['Name'])-1, 1)

#   ===============================================


def setHyperLink():
    dataset = [dict(file_names="images", location=r'C:/Users/thdharmakeerthi/Desktop/New folder (2)/Naive-Resume-Matching/Naive-Resume-Matching-master/Data/Resumes/images.png')]
    testDf = pd.DataFrame(dataset)

    def fun(path):
        f_url = os.path.basename(path)
        return '<a href="{}">{}</a>'.format(path, f_url)
    # Step 4 : applying make_clikable function

    df = testDf.style.format({'location': fun})
    return df


dataF = setHyperLink()

dataF
#   ===============================================

# create DopdownJdDictionary dictionary by following https://absentdata.com/python/how-to-create-a-dictionary-in-python-3-ways/
number = range(len(Jobs['Context']))
JdIndexList = list(number)
JdNameList = list(Jobs['Name'])
DopdownJdDictionary = dict(zip(JdIndexList, JdNameList))
# print("Dictionary :", DopdownJdDictionary)


def format_func(option):
    return DopdownJdDictionary[option]


option = st.selectbox("Select A Jd", options=list(
    DopdownJdDictionary.keys()), format_func=format_func)

st.write(f"You selected option {option} called {format_func(option)}")
index = option


option_yn = st.selectbox("Show the Job Description ?", options=['YES', 'NO'])
if option_yn == 'YES':
    JdObject = T6.CatagorizeByJdText(Jobs['Context'][index])
    st.markdown("---")
    st.markdown("### Job Description :")
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Job Role", "MustHaveSkills", "SecondarySkills", "Descreption"],
                    fill_color='#f0a500',
                    align='center', font=dict(color='white', size=16)),
        cells=dict(values=[JdObject.JobRole, JdObject.MustHaveSkills, JdObject.SecondarySkills, JdObject.Descreption],
                   fill_color='#f4f4f4',
                   align='left'))])

    fig.update_layout(width=800, height=500)
    st.write(fig)
    st.markdown("---")


#################################### SCORE CALCUATION ################################
# @st.cache_data
def calculate_scores(resumes, job_description):
    scores = []
    for x in range(resumes.shape[0]):
        score = Similar.match(
            resumes['TF_Based'][x], job_description['TF_Based'][index])
        scores.append(score)
    return scores


Resumes['Scores'] = calculate_scores(Resumes, Jobs)

Ranked_resumes = Resumes.sort_values(
    by=['Scores'], ascending=False).reset_index(drop=True)

Ranked_resumes['Rank'] = pd.DataFrame(
    [i for i in range(1, len(Ranked_resumes['Scores'])+1)])

###################################### SCORE TABLE PLOT ####################################

fig1 = go.Figure(data=[go.Table(
    header=dict(values=["Rank", "Name", "Scores"],
                fill_color='#00416d',
                align='center', font=dict(color='white', size=16)),
    cells=dict(values=[Ranked_resumes.Rank, Ranked_resumes.Name, Ranked_resumes.Scores],
               fill_color='#d6e0f0',
               align='left'))])

fig1.update_layout(title="Top Ranked Resumes", width=700, height=1100)
st.write(fig1)
