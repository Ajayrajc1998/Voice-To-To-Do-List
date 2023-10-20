import streamlit as st
import pandas as pd
from utls import audio_to_text, text_to_tasks
import json


# a='Schedule a meeting at 5am. remind me to feed mh dog at 10 am. reming me to call manager at 11pm'
# output = text_to_tasks(a)
# print(output)
# data = json.loads(output)

# # Create a DataFrame
# df = pd.DataFrame(data)
# print(df)
#Display the DataFrame

#Create a Streamlit button
st.write("Audio To Task Function")
if st.button("Process Audio and Extract Tasks"):
    # Call the process_audio function when the button is clicked
    a = audio_to_text()
    #a='Schedule a meeting at 5am. remind me to feed mh dog at 10 am. reming me to call manager at 11pm'
    output = text_to_tasks(a)
    data = json.loads(output)
    # Create a DataFrame
    df = pd.DataFrame(data)
    st.write("Task Table", df)