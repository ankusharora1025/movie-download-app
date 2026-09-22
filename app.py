import streamlit as st

st.set_page_config(
    page_title="Movie Download",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Download")

st.write("Download and watch movies from our collection.")

st.markdown("---")

st.subheader("🔥 Latest Movies")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("Movie 1")

with col2:
    st.info("Movie 2")

with col3:
    st.info("Movie 3")

with col4:
    st.info("Movie 4")
