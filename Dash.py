import streamlit as st
import plotly.express as das
import plotly.graph_objects as go
import pandas as pd

import os

st.set_page_config(page_title="First DashBorad",page_icon=":bar_chart:",layout="wide")


st.markdown(""" <style>
                div.block-container{padding:1rem;}
                </style>""",unsafe_allow_html=True)

st.title(":bar_chart: My DashBorad ")

upload = st.file_uploader(":file_folder: Upload File",type=(['csv','xlsx']))


if upload is not None:
    
    filename = upload.name
    st.write(filename)
    df = pd.read_csv(upload)
else:

    df = pd.read_csv(r"DATA.csv")    

col1 , col2 = st.columns((2))

df['Date'] = pd.to_datetime(df["Date"]).dt.date

startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    start = st.date_input("Start Date",startDate)
with col2:
    end = st.date_input("End Date",endDate)

df_filtered = df[(df["Date"] >= start) & (df["Date"] <= end) & (df["SupplierID"] != "Sugar 50kg")].copy()    


st.sidebar.header("Filter Panel")

# Filter Channel

channel = st.sidebar.multiselect("Channel",df["Channel"].unique())

if channel:
    df_filtered = df_filtered[df_filtered["Channel"].isin(channel)]

# Filter Supller

supplier = st.sidebar.multiselect("Supplier",df_filtered["SupplierID"].unique())    

if supplier:
    df_filtered = df_filtered[df["SupplierID"].isin(supplier)]

raw_data = df_filtered.copy()


_,sum1,sum2,sum3,_ = st.columns([0.5,1,1,1,0.5])

def format_number(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return f"{num:.0f}"

total_ctn = raw_data['QtyCtn'].sum()
total_amt = raw_data['AmountUSD'].sum()
total_cus = raw_data["CustomerID"].nunique(dropna=True)

def load_css():
    with open("test.css") as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

load_css()

with sum1:
    st.markdown(f"""
            <div class="metrix">
                <h4>Total Customer 🫡</h4>
                <h2>{format_number(total_cus)}</h2>
            </div>
                """, unsafe_allow_html=True)

with sum2:
    st.markdown(f"""
            <div class="metrix">
                <h4>Total CTN 🫡</h4>
                <h2>{format_number(total_ctn)}</h2>
            </div>
                """, unsafe_allow_html=True)


with sum3:
    st.markdown(f"""
            <div class="metrix">
                <h4>Total Amount 🫡</h4>
                <h2>{format_number(total_amt)}</h2>
            </div>
                """, unsafe_allow_html=True)




# Bar Chart ============================================================================

df_filtered = df_filtered.groupby("Channel",as_index=False)["AmountUSD"].sum()

with col1 :
    bar_chart = das.bar(df_filtered,x = "Channel",y="AmountUSD",text=["$ {:.2f}".format(x) for x in df_filtered['AmountUSD']])
    st.plotly_chart(bar_chart,use_container_width=True,height=400)

with col2:
    pie_chart = das.pie(df_filtered,names="Channel",values="AmountUSD",hole=0.5)
    # pie_chart.update_traces()
    st.plotly_chart(pie_chart,use_container_width=True,height=400)

cl1,cl2 = st.columns((2))    

with cl1:
    with st.expander("Channel_Data"):
        data = raw_data[raw_data['Channel'].isin(channel)] if channel else raw_data
       
        st.write(df_filtered)
        csv = data.to_csv(index=False,encoding="utf-8")
        st.download_button("Download Data",data=csv,file_name="Channel.csv",mime="csv/txt",
                           help="Click Button to download")

# linechart = raw_data
print(raw_data)
raw_data["YYY-MM"] = pd.to_datetime(raw_data["Date"]).dt.strftime("%d - %b")

linechart = (raw_data.groupby("YYY-MM")["AmountUSD"].sum()).reset_index()

linechart = das.line(linechart,x="YYY-MM",y="AmountUSD",labels={"YYY-MM":"AmounUSD"},width=400,height=400
                     ,text="AmountUSD",markers=True,title="Daily Sales")
linechart.update_traces(textposition="top center",texttemplate="%{text:.2~s}")

st.plotly_chart(linechart,use_container_width=True,height=400)
 

import plotly.figure_factory as ff

with st.expander("Summary Table"):
    table = raw_data[:10][["CustomerID","CustomerName","Phone","QtyCtn","AmountUSD"]]
    table_data = ff.create_table(table,colorscale="Cividis")
    raw_data["MonthName"] = pd.to_datetime(raw_data["Date"]).dt.month_name()
    st.plotly_chart(table_data,use_container_width=True,height=400)

    st.markdown("Table Summary")
    pivote = raw_data.pivot_table(aggfunc="sum",columns="MonthName",index=["SupplierID","ProductCat"],values="AmountUSD")
    # pivote.swaplevel(0,1,axis=1).sort_index(axis=1)
    st.write(pivote)

st.divider()

_,col_1 = st.columns([0.1,1])

combochart = raw_data.groupby("Date",as_index=False)[["AmountUSD","QtyCtn"]].sum().reset_index()

with col_1:

    fig = go.Figure()
    fig = fig.add_traces(go.Bar(x=combochart["Date"],y=combochart["AmountUSD"],name="AMount Sale",text=combochart["AmountUSD"],
                                texttemplate="%{text:.2~s}",textposition="outside",marker=dict(color="#4CAF50")))

    fig = fig.add_traces(go.Scatter(x=combochart["Date"],y=combochart["QtyCtn"],name="CTN Sale",
                                    text=combochart["QtyCtn"],mode="lines+markers",yaxis="y2",
                                    texttemplate="%{text:.2~s}",line=dict(color="#FF5733", width=3)))

    fig.update_layout(
        title="Total Sale",
        xaxis=dict(title="Date"),
        yaxis=dict(title ="USD",showgrid=False),
        yaxis2=dict(title="CTN",side="right",overlaying="y"),
        legend=dict(x=1,y=1)

    )
    # fig.update_traces()

    st.plotly_chart(fig,use_container_width=True,height=500)

    