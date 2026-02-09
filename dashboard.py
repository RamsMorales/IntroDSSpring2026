import streamlit as st
import pandas as pd
import plotly.express as px

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
        df = pd.read_csv("logs/biscayne_bay_water_quality2.csv")
    
    st.dataframe(df)
    #st.caption("Data collected from an underwater robot in biscayne bay on 02/13/2021\n\nThese data have been pre-cleaned.")
    st.divider()
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())
#--------------------------------------------------------------------------------------------------------------
#                                               tab 2: Charts
#--------------------------------------------------------------------------------------------------------------

with tab2:
    st.subheader("Charts")
    #expanders are like drop down "widgets"
    with st.expander("Heatmap"):
        feature1 = st.selectbox("Select First Parameter for Heat Map",df.columns)
        feature2 = st.selectbox("Select Second Parameter for Heat Map",df.columns)
        selected_df = df[[feature1,feature2]]
        corr = selected_df.corr(numeric_only=True)
        fig6 = px.imshow(corr,text_auto = True,
    title=f"Heatmap {feature1} vs {feature2}")
        st.plotly_chart(fig6)

    with st.expander("Box plot"):
        boxplotFeature = st.selectbox("Select distribution to see:",df.columns)
        fig7 = px.box(df,x=boxplotFeature)
        st.plotly_chart(fig7)

    with st.expander("Scatter plot"):
        fig1 = px.scatter(df,x="Total Water Column (m)",y="Temperature (c)",color="Salinity (ppt)",title="Temperature vs Total Water Column")
        ## The point is that aesthetic manipulation is done at the level of the fig object then st seems to handle rendering given the objects features 
        st.plotly_chart(fig1)
        #We will have to clean the data for visualization.
    with st.expander("Line Chart"):
        fig2 = px.line(df,x="Time",y="Temperature (c)",title="Temperature over Time")
        st.plotly_chart(fig2)    
    ## an interesting idea. Allowing the user to select which features to map and colors -> dashboard creation
    with st.expander("Make your own (Line Chart) vs Time"):
        col1,col2 = st.columns([1,4])
        with col1:
            selected_feature = st.selectbox("Select a Parameter:",df.columns)
            color_selected = st.color_picker("Select a color:","#6495ED")
        with col2:
            fig3 = px.line(df,x="Time",y=selected_feature,title=f"{selected_feature} vs Time",color_discrete_sequence=[color_selected])
            st.plotly_chart(fig3)

    with st.expander("3D plot"):
        fig4 = px.scatter_3d(df,x="Longitude",y="Latitude",z="Total Water Column (m)",color="pH",title="pH Along Robot Trajectory")
        fig4.update_scenes(zaxis_autorange="reversed")
        st.plotly_chart(fig4)
#--------------------------------------------------------------------------------------------------------------
#                                               tab 3: Maps
#--------------------------------------------------------------------------------------------------------------
with tab3:
    st.subheader("Maps")
    fig5 = px.scatter_mapbox(df,lon="Longitude",lat="Latitude",color="Temperature (c)",mapbox_style="open-street-map",zoom=17,hover_data=df,color_continuous_scale=px.colors.diverging.Picnic)
    st.plotly_chart(fig5)
    st.caption("Map of robot path. Hover over the data points to learn more!")