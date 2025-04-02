import streamlit as st 
import numpy as np 
import pandas as pd 

st.title("Streamlit App")

st.write("Streamlit application for testing")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [8, 9, 10, 11]
})
st.write('Dataframe:')
st.write(df)

chart_data = pd.DataFrame(
    np.random.randn(10, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)