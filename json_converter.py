import io
import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="JSON to CSV & Parquet", page_icon="🧾", layout="centered")
st.title("JSON to CSV & Parquet Converter")

uploaded = st.file_uploader("Upload a JSON file", type=["json"])

def load_json_to_df(file) -> pd.DataFrame:
    obj = json.load(file)
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    elif isinstance(obj, dict):
        try:
            return pd.json_normalize(obj)
        except Exception:
            return pd.DataFrame([obj])
    else:
        raise ValueError("Unsupported JSON: upload a list of objects or a flat dict.")

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def df_to_parquet_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_parquet(buf, engine="pyarrow", index=False)
    return buf.getvalue()

if uploaded:
    try:
        df = load_json_to_df(uploaded)
    except Exception as e:
        st.error(f"Failed to read JSON: {e}")
        st.stop()

    st.success(f"Loaded JSON → DataFrame shape {df.shape}")
    st.dataframe(df.head(100), use_container_width=True)

    st.subheader("Download Converted Formats")
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download CSV",
            data=df_to_csv_bytes(df),
            file_name="converted.csv",
            mime="text/csv"
        )

    with col2:
        st.download_button(
            "Download Parquet",
            data=df_to_parquet_bytes(df),
            file_name="converted.parquet",
            mime="application/octet-stream"
        )
else:
    st.info("Upload a JSON file to begin.")