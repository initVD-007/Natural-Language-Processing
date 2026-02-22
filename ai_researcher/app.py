import streamlit as st
from parsers import AgentA_Parser
from scout import AgentB_Scout
from auditor import AgentC_Auditor
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

if st.session_state.get('agent_a_report'):
    report = st.session_state['agent_a_report']
    if st.button("Let Agent B Scout 2026 Trends"):
        parser = AgentA_Parser()
        queries = parser.get_search_queries(report)

        # 2. running the scout
        scout = AgentB_Scout()
        with st.spinner("Agent B is searching a live web...."):
            web_data = scout.search_2026(queries)
            st.session_state['web_data'] = web_data

        st.subheader("Agent B: Real-Time Findings")
        for res in web_data:
            st.write(f"**Query:** {res['query']}")
            for f in res['findings']:
                st.write(f"- {f}")

if 'web_data' in st.session_state:
    if st.button("Run Final Audit (Agent c)"):
        auditor = AgentC_Auditor()

        #preparing tha data for agent C
        syllabus_info = st.session_state['agent_a_report']
        web_info = str(st.session_state['web_data']) # Convert search list to string

        with st.spinner("Agent C is auditing the curriculum gap..."):
            final_report = auditor.generate_audit_report(syllabus_info, web_info)
        
        st.divider()
        st.header("Final Modernization Report")
        st.markdown(final_report)

        # Add a download button for the professor
        st.download_button("Download Report", final_report, file_name="final_report.txt")


    
