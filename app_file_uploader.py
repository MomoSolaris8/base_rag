"""
based Streamlit web app
"""
import streamlit as st

st.title("knowledge update service")

# file_uploader
upload_file = st.file_uploader(
    "Upload a file",
    type=["txt"],
    accept_multiple_files=False,
)

if upload_file is not None:

    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    st.subheader(f"File name: {file_name}")
    st.write(f"File type: {file_type}| File size: {file_size:.2f} KB")

    #get_value-> bytes-> decode('utf-8')'
    text= upload_file.getvalue().decode()
    st.write(text)