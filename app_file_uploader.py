"""
based Streamlit web app
Streamlit reruns the entire script whenever a widget or
  page element changes, which means normal local variables do
  not persist between interactions.
"""


import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

st.title("knowledge update service")

# file_uploader
upload_file = st.file_uploader(
    "Upload a file",
    type=["txt"],
    accept_multiple_files=False,
)
service = KnowledgeBaseService()
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if upload_file is not None:

    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024

    st.subheader(f"File name: {file_name}")
    st.write(f"File type: {file_type}| File size: {file_size:.2f} KB")

    #get_value-> bytes-> decode('utf-8')'
    text= upload_file.getvalue().decode("utf-8")

    with st.spinner("uploading..."):
        time.sleep(1)
        result= st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)


   # st.write(text)
   # st.session_state["counter"] += 1

#print(f"upload: {st.session_state['counter']} files")