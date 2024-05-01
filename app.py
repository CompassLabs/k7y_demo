import streamlit as st
import os
from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account

load_dotenv()

st.set_page_config(layout="wide")

with st.container(border=True):
    st.title("Data explorer")
    num_blocks = 100000
    start_block = st.slider(
        label=f"Select the starting block. We display {num_blocks} blocks at a time...",
        min_value=13000000,
        max_value=19000000,
        value=15000000,
        step=num_blocks,
        label_visibility="visible",
    )


info = {
    "type": "service_account",
    "project_id": "dojo-405216",
    "private_key_id": os.getenv("GCP_KEY_ID"),
    "private_key": os.getenv("GCP_KEY"),
    "client_email": "dojo-blob-uploader@dojo-405216.iam.gserviceaccount.com",
    "client_id": "107342926184084873838",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dojo-blob-uploader%40dojo-405216.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}

credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = bigquery.Client(credentials=credentials)


with st.container(border=True):
    st.subheader("function-call data")
    st.text(
        "We can get the result of function calls for a any contract and function name"
    )
    query = f"""
    SELECT
        block,
        function_name,
        inputs,
        outputs,
    FROM `dojo-405216.dojo_backtest_data.call_data`
    WHERE contract="0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
        AND function_name="slot0"
        AND block > {start_block}
        AND block < {start_block+num_blocks}
    ORDER BY block
    """
    st.code(query, language="sql")
    with st.spinner():
        df = client.query(query).result().to_dataframe()
        st.dataframe(df, use_container_width=True)


with st.container(border=True):
    st.subheader("event data")
    st.text("We can gather all event data for any contract in a given block range")
    query2 = f"""
    SELECT 
        *
    FROM `dojo-405216.dojo_backtest_data.events`
        WHERE contract="0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
        AND block > {start_block}
        AND block < {start_block+num_blocks}
    ORDER BY block
    """
    st.code(query, language="sql")
    with st.spinner():
        df2 = client.query(query2).result().to_dataframe()
        st.dataframe(df2, use_container_width=True)
