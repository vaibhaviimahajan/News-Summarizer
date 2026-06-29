from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(
    page_title="AI News Summarizer",
    page_icon="📰",
    layout="centered"
)
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0B1F3A;
    color: white;
}

/* Make all text white */
h1, h2, h3, h4, h5, h6, p, label, div {
    color: white !important;
}

/* Input box */
.stTextInput input {
    background-color: #1C355E;
    color: white;
    border-radius: 10px;
    border: 1px solid #4A6FA5;
}

/* Button */
.stButton>button {
    width: 100%;
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #1D4ED8;
}

/* Expander */
.streamlit-expanderHeader {
    color: white !important;
}

/* Success message */
.stSuccess {
    background-color: #163D6B;
}

</style>
""", unsafe_allow_html=True)

st.title("📰 AI News Summarizer")

st.write("Enter any topic to get the latest news summarized by AI.")

topic = st.text_input("Topic", placeholder="Artificial Intelligence")

if st.button("Summarize News"):

    with st.spinner("Searching latest news..."):

        search_tool = TavilySearchResults(max_results=5)

        llm = ChatMistralAI(model="mistral-small-2506")

        prompt = ChatPromptTemplate.from_template("""
You are an expert news analyst.

Summarize the following news into concise bullet points.

News:

{news}
""")

        chain = prompt | llm | StrOutputParser()

        news = search_tool.run(f"Latest {topic} news")

        summary = chain.invoke({"news": news})

    st.success("Done!")

    st.subheader("Summary")

    st.write(summary)

    with st.expander("Original Search Results"):

        st.write(news)