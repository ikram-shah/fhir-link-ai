import streamlit as st

from sidebar import setup as set_sidebar
from langchain.llms import OpenAI
from langchain.chains import OpenAPIEndpointChain

from utils import (
    set_headers,
    clear_submit,
    paths_and_methods,
    set_logo_and_page_config,
    check_all_config
)

set_logo_and_page_config()
set_sidebar()

st.write("OpenAI API Key added:", st.session_state.get("OPENAI_API_KEY") != None)
st.write("FHIR Server details added:", st.session_state.get("FHIR_API_BASE_URL") != None)

if check_all_config():
    operation = paths_and_methods()

    llm = OpenAI(openai_api_key=st.session_state.get("OPENAI_API_KEY")) 

    # headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": "true", }
    request_wrapper = set_headers()
    chain = OpenAPIEndpointChain.from_api_operation(operation,llm,requests=request_wrapper,verbose=True)

    query = st.text_area("Search Input", label_visibility="visible", placeholder="Ask anything...", on_change=clear_submit)

    button = st.button("Search")

    if button or st.session_state.get("submit"):
        if not st.session_state.get("is_key_configured"):
            st.error("Please configure your OpenAI API Key!", icon="🚨")
        elif not query:
            st.error("Please enter an input!", icon="🚨")
        else:
            st.session_state["submit"] = True
            with st.spinner(text="Searching..."):
                result = chain(query)
                st.write("#### Answer")
                st.write(result["output"])