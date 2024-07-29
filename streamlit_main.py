import configparser
import pandas as pd
import streamlit as st
import boto3

#streamlit run streamlit_main.py in terminal

config = configparser.ConfigParser()
config.read('aws.cfg')
AWS_ACCESS_KEY = config['AWS']['aws_access_key']
AWS_SECRET_KEY = config['AWS']['aws_secret_key']

s3_client = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

# output = s3_client.download_file(Bucket= 'capstone-techcatalyst-raw', Key='yellow_taxi/yellow_tripdata_2023-09.parquet', Filename='09-2023-yellow-taxi.parquet')

st.title('NYC Taxi Data Analysis')
df = pd.read_parquet('09-2023-yellow-taxi.parquet')

cols = st.multiselect('Select Columns', df.columns)

if st.checkbox("Show Data"):
    st.dataframe(df[cols].head(20))

file = st.file_uploader("Upload your CSV data", type=["csv"])
st.write(file)

ts = df[['tpep_pickup_datetime', 'total_amount']]
ts['date'] = ts['tpep_pickup_datetime'].dt.date
ts_sum = ts.groupby('date')[['total_amount']].mean()
ts_sum.reset_index(inplace=True)
ts_sum['date'] = pd.to_datetime(ts_sum['date'])

if st.checkbox('Show Line Chart'):
    st.line_chart(ts_sum.set_index('date'))

st.write('Top 10 Pickup Locations')
st.dataframe(df['PULocationID'].value_counts().head(10))
st.bar_chart(df['PULocationID'].value_counts().head(10))

st.write('Filter Data by payment type')
payment = st.selectbox('Payment Type', df['payment_type'].unique())
st.write(df[df['payment_type'] == payment])

df2 = pd.read_parquet('09-2023-yellow-taxi.parquet').head(100)
data = st.data_editor(df2)
st.balloons()
