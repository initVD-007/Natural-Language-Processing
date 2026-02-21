import streamlit as st
from parsers import AgentA_Parser

#1. Page Config.
st.set_page_config(page_title="Universal Syllabus Researcher", layout="wide")
st.title("Universal Syllabus Researcher")
st.write("Modernizing any curriculum using Multi-Agent AI (2026 Standards)")

#2. side bar for instructions
with st.sidebar:
    st.header("How to Use")
    st.info("Upload any PDF or PPTX syllabus. Agent A will parse it and identify the subject automatically")

#3. File uploader
uploaded_file = st.file_uploader("Upload Syllabus (PDF or PPTX)", type=["pdf", "pptx"])

if uploaded_file:
    # Initialize our Agent A Parser
    parser = AgentA_Parser()

    with st.status("Agent A is working....", expanded=True) as status:
        st.write("Reading file contents...")
        text_data = parser.extract_text(uploaded_file)

        st.write("Performing Semantic Analysis...")
        report = parser.analyze_content(text_data)

        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # Display Results in a nice  layout
    st.divider()
    st.subheader("Agent A: Parser Report")
    st.markdown(report)

    # Save the report in 'session_state' so Agent B can access it later
    st.session_state['agent_a_report'] = report
    st.success("Data ready for Agent B (The Scout)!")


    
