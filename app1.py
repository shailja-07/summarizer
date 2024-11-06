import streamlit as st
from langchain.chains.llm  import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from fpdf import FPDF
from docx import Document
import io


model_name = "facebook/bart-large-cnn"
llm = HuggingFaceHub(repo_id=model_name, huggingfacehub_api_token=st.secrets["api_key"])



st.title("Text Summarizer")
st.header("Enter the text you want to summarize")
st.divider()

text = st.text_area("Provide the text to summarize:", "Enter text here...")

st.divider()


prompt = ChatPromptTemplate.from_messages(
    [("system", "Write a concise summary of the following:\n\n{context}")]
)


llm_chain = LLMChain(llm=llm, prompt=prompt)

if text:
  
    summary = llm_chain.invoke({"context": text})
    
    
    summary_text = summary.get('text', summary) if isinstance(summary, dict) else summary

   
    if not isinstance(summary_text, str):
        summary_text = str(summary_text)

   
    st.write("**Summary:**")
    st.write(summary_text)

   
    st.download_button(
        label="txt file",
        data=summary_text,
        file_name="summary.txt",
        mime="text/plain",
    )

   
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)


    pdf.multi_cell(0, 10, summary_text.encode('latin-1', 'replace').decode('latin-1'))

   
    pdf_output = pdf.output(dest='S').encode('latin-1')
    
    st.download_button(
        label="pdf file",
        data=pdf_output,
        file_name="summary.pdf",
        mime="application/pdf",
    )

  
    doc = Document()
    doc.add_paragraph(summary_text)

   
    doc_stream = io.BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0) 

    st.download_button(
        label="docx file",
        data=doc_stream,
        file_name="summary.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

st.divider()