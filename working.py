import pandas as pd

data = {
    'tasks': [
        {'timestamp': '11:00 a.m.', 'completed': False, 'Task': 'Schedule a meeting', 'level of importance': 'medium', 'task_id': '1'},
        {'timestamp': '12:00 p.m.', 'completed': False, 'Task': 'Schedule a meeting', 'level of importance': 'medium', 'task_id': '2'},
        {'timestamp': '03:00 p.m.', 'completed': False, 'Task': 'Schedule a meeting', 'level of importance': 'medium', 'task_id': '3'},
        {'timestamp': '05:00 p.m.', 'completed': False, 'Task': 'Feed my dog', 'level of importance': 'medium', 'task_id': '4'},
        {'timestamp': '10:00 p.m.', 'completed': False, 'Task': 'Remind me to sleep', 'level of importance': 'medium', 'task_id': '5'}
    ]
}

# Extract 'tasks' list from the data
tasks_data = data['tasks']

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(tasks_data)

# Display the DataFrame

import streamlit as st
st.write(df)

