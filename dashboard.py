import streamlit as st
import pandas as pd

#recall to run dashboard
#    streamlit run dashboard.py

#    or 

#    python3 -m streamlit run dashboard.py


#--------------------------------------------------------------------------------------------------------------
#                                               Title
#--------------------------------------------------------------------------------------------------------------
st.title("Water Data Dashboard")
st.header("Spring 2026")
st.subheader("Ramson Munoz Morales")
st.divider()

st.sidebar.header("Load Datasets")
file_uploaded = st.sidebar.file_uploader("Upload a file",type=["csv"])

#--------------------------------------------------------------------------------------------------------------
#                                               tabs
#--------------------------------------------------------------------------------------------------------------

tab1,tab2,tab3 = st.tabs(["raw data","charts", "maps"])

#--------------------------------------------------------------------------------------------------------------
#                                               tab 1: Raw data
#--------------------------------------------------------------------------------------------------------------

with tab1:
    st.subheader("Raw Data")
    if file_uploaded is not None:
        df = pd.read_csv(file_uploaded)
    else:
        df = pd.read_csv("logs/biscayne_bay_water_quality.csv")
    
    st.dataframe(df)
    #st.caption("Data collected from an underwater robot in biscayne bay on 02/13/2021\n\nThese data have been pre-cleaned.")
    st.divider()
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

