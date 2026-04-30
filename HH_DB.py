import pandas as pd
import plotly.express as px
import streamlit as st
from Get_Data import raw_data as data
# from formart_db import format_number


import datetime

import formart_db

# data.to_csv(r"D:\Year 2026\import.csv")



# Load CSS
def load_css():
    with open("honghuot.css") as f:
        st.markdown(
            f"""
                <style>
                    {f.read()}
                </style>
            """,unsafe_allow_html=True
        )



load_css()

st.markdown(
    """<style>
        div.block-container{
            padding: 10px;
        }
        </style>""",unsafe_allow_html=True
)

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.2f} M"
    elif num >=1000:
        return f"{num/1000:.2f} K"
    elif num < 1000 :
        return f"{num:.2f}"
def format_amount(num):
        return f"$ {num:,.2f}"

data['QtyCtn'] = data['QtyCtn'].astype(float)
data['AmountUSD'] = data['AmountUSD'].astype(float)


st.set_page_config(page_title="HONG HUOT",layout="wide",page_icon="🆕")
st.title("📈 HONG HOUT DASHBORAD",)


with st.sidebar:
    st.header("DATA FILTER",divider=True)

    # Take Stock 
    select_takestock = ["All","HH"]
    takestock = st.selectbox("Take Stock",select_takestock,)
    # Set Year Filter
    year = pd.DataFrame(data['YYYY'].unique())
    _year = st.multiselect("Year",year,default=year.max())

    # Set Month Filter
    data["MonthName"] = pd.to_datetime(data['Date']).dt.month_name()
    sort_data = data.sort_values(by="MM",ascending=True)
    uni_month = sort_data['MonthName'].unique()
    last_month = sort_data["MonthName"].iloc[-1]
    _month = st.multiselect("Month",uni_month,default=last_month)

    # Set Channel
    fil_channel = data["Channel"].unique()
    _channel = st.multiselect("Channel",fil_channel)

_,sum1,sum2,sum3,sum4,_ = st.columns([0.1,1,1,1,1,0.1])


# Data Filtered

filtered_data = data[data["SupplierID"] != "Sugar 50kg"].copy()


if takestock == "HH":
    filtered_data = filtered_data[filtered_data["TakeStock"] == takestock]



if _year:  
    filtered_data = filtered_data[filtered_data["YYYY"].isin(_year)]

filter_yearly = filtered_data.copy()
    

if _month:
    filtered_data = filtered_data[filtered_data["MonthName"].isin(_month)]

# Set Filter Supplier By Channel
filter_channel = filtered_data.copy()

if _channel:
    filter_channel= filter_channel[filter_channel['Channel'].isin(_channel)]
    filter_yearly = filter_yearly[filter_yearly['Channel'].isin(_channel)]

# st.map()
with sum1:
    totol_customer = filtered_data["CustomerID"].nunique(dropna=True)
    st.info("Total Customer")
    st.markdown(
        f"""
            <div class="summary_box">
                <h4>Active Customer</h4>
                <h1>{format_number(totol_customer)}</h1>
            </div>
        """,unsafe_allow_html=True
    )
with sum2:
    totol_sku = filtered_data["ItemName"].nunique(dropna=True)
    st.info("Total SKUs")
    st.markdown(
        f"""
            <div class="summary_box">
                <h4>Active SKUs</h4>
                <h1>{format_number(totol_sku)}</h1>
            </div>
        """,unsafe_allow_html=True
    )
with sum3:
    totol_ctn = filtered_data["QtyCtn"].sum()
    st.info("Total CTN")
    st.markdown(
        f"""
            <div class="summary_box">
                <h4>Active CTN</h4>
                <h1>{format_number(totol_ctn)}</h1>
            </div>
        """,unsafe_allow_html=True
    )
with sum4:
    totol_amount = filtered_data["AmountUSD"].sum()
    st.info("Total Amount")
    st.markdown(
        f"""
            <div class="summary_box">
                <h4>Active Amount</h4>
                <h1>{format_number(totol_amount)}</h1>
            </div>
        """,unsafe_allow_html=True
    )

# Start Analysis and Chart
ch1,ch2 = st.columns((2))

channel = filtered_data.groupby("Channel")['AmountUSD'].sum().reset_index()

# USe Data Filter Channel
supllier = filter_channel.groupby("SupplierID")['AmountUSD'].sum().reset_index()
supllier = supllier.sort_values(by="AmountUSD",ascending=True)

product_company = filter_channel.groupby("CompanyID")["AmountUSD"].sum().reset_index()

with ch1:
    bar = px.bar(channel,x="Channel",y="AmountUSD",title="Channel Sales",)
    bar.update_traces(
        texttemplate="%{y:.2s}",
       
    )
    st.plotly_chart(bar,use_container_width=True,height=500)

with ch2:
    pie = px.pie(product_company,names="CompanyID",values="AmountUSD",
                 title="Product Company",labels="CompanyID",
                 hole=0.2)
    pie.update_traces(
      
        textinfo="value+percent+label"
       
    )
    st.plotly_chart(pie,use_container_width=True,height=500)

# Create Horizonetal Bar Chart
bar = px.bar(supllier,x="AmountUSD",y="SupplierID",title="SupplierID",orientation="h")
bar.update_traces(
    texttemplate="%{x:,.2s}",
    textfont=dict(size=20),
    textposition="outside"
    
)
bar.update_layout(
    xaxis = dict(title="Amount",tickfont=dict(size=16)),
    yaxis = dict(tickfont=dict(size=16),title=""),
    font=dict(size=20),
    margin=dict(l=70,r=70,b=0,t=40)
)
st.plotly_chart(bar,use_container_width=True,height=500)

_,detail,_ = st.columns([0.2,1,0.2])
with detail:
    with st.expander("Detail By Product Category"):
        
        st.title("Product",width=250)
        by_cate = filter_channel[filter_channel["QtyCtn"] > 0].groupby(
            ["SupplierID","ProductCat","ItemName"])[["QtyCtn","AmountUSD"]].sum().reset_index()
        
        st.dataframe(by_cate,
                     column_config={"AmountUSD":st.column_config.NumberColumn("AmountUSD",format="accounting"),
                                    "QtyCtn":st.column_config.NumberColumn("QtyCtn",format="accounting")
                                    })
        # st.write(by_cate)
st.divider()
# Create Daily Sale Line Chart
filter_channel["DD-MM"] = pd.to_datetime(filter_channel["Date"]).dt.strftime("%d-%b")
daily_sale = filter_channel.groupby("DD-MM")["AmountUSD"].sum().reset_index()

line = px.line(daily_sale,x="DD-MM",y="AmountUSD",title="Daily Sales",text="AmountUSD")

line.update_traces(
    texttemplate="%{y:,.2s}",
    textposition="top center"
)
st.plotly_chart(line,use_container_width=True,height=500)

with st.expander("Detail Daily Sale "):
    
    daily = filter_channel[filter_channel["QtyCtn"] > 0].pivot_table(aggfunc="sum",
                                       index=["SupplierID","ProductCat","ItemName"],
                                       columns=["DD-MM"],
                                       values=["QtyCtn","AmountUSD"],
                                       fill_value=0,
                                       sort=True
                                       
                                       )
    # daily.columns = pd.MultiIndex.from_tuples([(col1,col2) for col1,col2 in daily.columns])
    daily.columns = [f"{col1.replace("Amount","").replace("Qty","")} | {col2}" for col1,col2 in daily.columns]
    daily = daily.reset_index().set_index(["SupplierID","ProductCat","ItemName"])
    st.title(f"Daily Sale {_channel}")
    st.dataframe(daily.style.format("{:,.2f}")
                 
                 )
    

st.divider()
# Creat Bar Chart Monthly
import plotly.graph_objects as go

filter_yearly["MM-YYYY"] = pd.to_datetime(filter_yearly["Date"]).dt.strftime("%b-%Y")

by_monthly = filter_yearly.groupby(["MM-YYYY","MM","YYYY"])["AmountUSD"].sum().reset_index()
by_monthly = by_monthly.sort_values(by=["YYYY","MM"],ascending=[True,True]).reset_index()
monthly_chart = go.Figure()
monthly_chart = monthly_chart.add_traces(go.Bar(x=by_monthly["MM-YYYY"],y=by_monthly["AmountUSD"],
                                                text=by_monthly["AmountUSD"],
                                                name="Monthly Amount",texttemplate="%{text:.2~s}"))
monthly_chart.update_layout(
    title="Monthly Sales",
    font=dict(size=16),
    xaxis=dict(tickfont=dict(size=16)),
    yaxis=dict(tickfont=dict(size=16)),
)
st.plotly_chart(monthly_chart,use_container_width=True,height=500)