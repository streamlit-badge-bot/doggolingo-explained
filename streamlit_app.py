import streamlit as st
import numpy as np
import pandas as pd 
import pickle
import random
import re 
import csv

#st.title('DOGGOLINGO')
st.markdown("<h1 style='text-align: center; color: blue;font-family:arial;'>DOGGOLINGO</h1>", unsafe_allow_html=True)

st.write("Dogs (and dog-people) have their own language on the internet, but it's not always easy to keep up with the ever-evolving dialect.")

#st.image('dogcloud.png',width=500)

st.write("Fortunately, a picture is worth a thousand words. Select a term below to see how it's used in images and in text!")

# read in terms data
# terms = []
# with open('app_terms.csv', newline='') as inputfile:
#     for row in csv.reader(inputfile):
#         terms.append(row[0])
terms = pd.read_csv('app_terms.csv',header=None)
terms = list(terms[0])

#st.write(terms)

# create selectbox 
term = st.selectbox("Select a term to see how it's used:",terms)

# read in image dataframe
df = pickle.load(open("url_df.pickle", "rb"))

# posts that contain the selected term
term_posts = df[df['clean_comments'].str.contains(term)]

st.title('In images...')
# get first three images
#images = list(term_posts['img_url'])

st.markdown('*NOTE: may contain NSFW images. Explore at your own risk.*')

# display first three images
if len(term_posts.index) >=3:
    random_three_img = term_posts.sample(3)
    #random_three_img = random.sample(term_posts,3)
    for idx, row in random_three_img.iterrows():
        st.image(row['img_url'],width=215,caption=(row['author']+" / via reddit.com"), use_column_width=True)
else:
    st.write("Oops! No images found. Try another term.")
    st.image('https://images.unsplash.com/photo-1453227588063-bb302b62f50b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1050&q=80',width=400)


st.title('In a sentence...')
texts = list(term_posts['full_comments'])

# print some sentences
## note: try to add functionality to print string nearby if sentence pattern doesn't match
## fix the randomization also
random_texts = random.sample(texts,len(texts))
#st.write('random texts',random_four_texts)
all_sentences = []
for text in random_texts:
    text_sentences = re.findall("[^.?!]*(?<=[.?\s!])"+term+"(?=[\s.?!])[^.?!]*[.?!]",text)
    for t in text_sentences:
        all_sentences.append(t)
#st.write('all sentences',all_sentences)
counter = 0
for i in range(0,6):
    try: 
        st.write('"'+all_sentences[i]+'"')
    except:
        pass
    # for s in all_sentences:
    #     st.write('"'+s+'"')
    #     counter += 1
if len(all_sentences) == 0:
    st.write("Oops! No text found. Try another term.")