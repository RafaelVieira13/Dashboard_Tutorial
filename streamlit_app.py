import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import warnings 
warnings.filterwarnings('ignore')
import os

# Dashboard Title
st.set_page_config(page_title='Superstore!!',page_icon=':bar_chart:',layout='wide')
st.title(' :bar_chart: Sample Superstore EDA')
st.markdown('<style>div.block-container{padding-top:1rem}<style>',unsafe_allow_html=True)

# Create a place to upload a file a read the data
fl = st.file_uploader(':file_folder: Upload a File',type=(['csv','txt','xlsx','xls']))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r'C:\Users\Administrador\OneDrive\Ambiente de Trabalho\Dashborad_Tutotrial')
    df = pd.read_excel('Sample - Superstore.xls')

# Let´s Create a Column 1 and a Column 2
col1, col2 = st.columns((2))

# Convert the Order Date Column into Datetime type in order to create a schedule
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Get the min and max date for the schedule
startDate = pd.to_datetime(df['Order Date'].min())
endDate = pd.to_datetime(df['Order Date'].min())

# Let's Create a Schedule for the StratDate in the column 1
with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))

# Let's Create a Schedule for the EndDate in the column 2
with col2:
    date2 = pd.to_datetime(st.date_input('End Date',endDate))

# Update the date based on the startdate and enddate chosed in the schedule
df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

# Create a side bar filter to filter the data based on the Region, Sate and City

# Region
st.sidebar.header('Choose your filter: ')
region = st.sidebar.multiselect('Pick the Region', df['Region'].unique())
    # In the case to not choose any region use all data else use the filter region data
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

# State
state = st.sidebar.multiselect('Pick the State', df['State'].unique())
    # In the case to not choose any state use all data else use the filter state data
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

# City
city = st.sidebar.multiselect('Pick the City', df3['City'].unique())


# Filter the data Based on Region, State and City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(region) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

# Create a Bar Chart displaying The Sales By Product Category Based on The Region, State and City
category_df = filtered_df.groupby(by=['Category'], as_index=False)['Sales'].sum()

with col1:
    st.subheader('Category wise Sales')
    fig = px.bar(category_df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']],
                 template='seaborn')
    st.plotly_chart(fig, use_container_width=True, height=400)

# Pie Chart with Region Sales
with col2:
    st.subheader('Region wise Sales')
    fig = px.pie(filtered_df, values = 'Sales', names = 'Region', hole = 0.5)
    fig.update_traces(text = filtered_df['Region'], textposition = 'outside')
    st.plotly_chart(fig, use_container_width=True)

# Let´s Create a Tabel With a Button to Upload the Data Used for the Bar Chart and Pie Chart Based on the Filter Choices
cl1, cl2 = st.columns(2)

with cl1:
    with st.expander('Category_ViewData'):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index=False)
        st.download_button('Download Data', data = csv, file_name='Category.csv', mime = 'text/csv',
                           help = 'Click here to download the data as a CSV file')
    
with cl2:
    with st.expander('Region_ViewData'):
        region = filtered_df.groupby(by = 'Region', as_index=False)['Sales'].sum()
        st.write(region.style.background_gradient(cmap='Oranges'))
        csv = region.to_csv(index=False)
        st.download_button('Download Data', data = csv, file_name='Region.csv', mime = 'text/csv',
                           help = 'Click here to download the data as a CSV file')
        
# Let´s Create a Line Plot to Display The Sales By Each Month
filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader('Sales Per Month')
linechart = pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum()).reset_index()
fig2 = px.line(linechart, x= 'month_year', y = 'Sales', labels = {'Sales':'Amount'}, height=500, width = 1000, template = 'gridon')
st.plotly_chart(fig2, use_container_width=True)

with st.expander('View Data of Sales Per Month:'):
    st.write(linechart.T.style.background_gradient(cmap='Blues'))
    csv = linechart.to_csv(index=False)
    st.download_button('Download Data', data = csv, file_name = 'SalesPerMonth.csv', mime='text/csv')

# Let´s Create 2 Pie Charts for Segement The Sales and for Category Sales
chart1, chart2 = st.columns((2))

with chart1:
    st.subheader('Segment Wise')
    fig = px.pie(filtered_df, values = 'Sales', names = 'Segment',template='plotly_dark')
    fig.update_traces(text = filtered_df['Segment'], textposition = 'inside')
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Category Wise')
    fig = px.pie(filtered_df, values = 'Sales', names = 'Category',template='gridon')
    fig.update_traces(text = filtered_df['Category'], textposition = 'inside')
    st.plotly_chart(fig, use_container_width=True)

# Let´s Create a Tabel Summary
st.subheader(':point_right: Month Wise Sub-Category Sales Summary')
with st.expander('Summary_Table'):
    df_sample = df[0:5][['Region','State','City','Sales','Profit','Quantity']]
    fig = ff.create_table(df_sample, colorscale = 'cividis')
    st.plotly_chart(fig, use_container=True)

    # Let´s Create a Month Wise Sub-Category Table
    st.markdown('Month wise Sub-Category Table')
    filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
    sub_category_year = pd.pivot_table(data = filtered_df, values = 'Sales', index=['Sub-Category'], columns = 'month')
    st.write(sub_category_year.style.background_gradient(cmap='Blues'))

# Let´s Create a Scatter Plot to display 'Sales' vs 'Profit'
data1 = px.scatter(filtered_df, x='Sales', y='Profit', size= 'Quantity')
data1['layout'].update(title='Relastionship Between Sales and Profit',
                       titlefont = dict(size=20),
                       xaxis = dict(title='Sales', titlefont=dict(size=19)),
                       yaxis = dict(title='Profit', titlefont= dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

# Viwe The Top 500 Rows and Columns From 1 to 20 and Stepwise 2 of the  Dataset and Create a Button to Download it
with st.expander('View Data'):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap='Oranges'))

# Download the Original Dataset
csv =df.to_csv(index=False)
st.download_button('Download the Original Data', data=csv, file_name='Data.csv', mime='text/csv')

