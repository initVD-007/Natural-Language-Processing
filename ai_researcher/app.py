import streamlit as st
from parsers import AgentA_Parser
from scout import AgentB_Scout
from auditor import AgentC_Auditor

# 1. Page Config.
st.set_page_config(page_title="Universal Syllabus Researcher", layout="wide")
st.title("Universal Syllabus Researcher")
st.write("Modernizing any curriculum using Multi-Agent AI (2026 Standards)")

def clear_session():
    # Clear session state when a new file is uploaded or reset is clicked
    for key in list(st.session_state.keys()):
        if key not in ['google_api_key', 'serper_api_key']:
            del st.session_state[key]

# 2. Side bar for instructions & Configuration
with st.sidebar:
    st.header("Configuration ⚙️")
    google_api_key = st.text_input("Google Gemini API Key", type="password", help="Get this from Google AI Studio")
    serper_api_key = st.text_input("Serper API Key", type="password", help="Get this from serper.dev")
    
    st.session_state['google_api_key'] = google_api_key
    st.session_state['serper_api_key'] = serper_api_key

    st.markdown("---")
    st.header("How to Use")
    st.info("Upload any PDF or PPTX syllabus. Agent A will parse it and identify the subject automatically")
    
    if st.button("Reset Application"):
        clear_session()
        st.rerun()

# Stop execution if API keys are missing
if not st.session_state['google_api_key'] or not st.session_state['serper_api_key']:
    st.warning("⚠️ Please enter both Google Gemini and Serper API Keys in the sidebar to continue.")
    st.stop()

# 3. File uploader
uploaded_file = st.file_uploader("Upload Syllabus (PDF or PPTX)", type=["pdf", "pptx"], on_change=clear_session)

if uploaded_file:
    # Agent A Processing
    if 'agent_a_report' not in st.session_state:
        try:
            parser = AgentA_Parser(st.session_state['google_api_key'])
            with st.status("Agent A is working...", expanded=True) as status:
                st.write("Reading file contents...")
                text_data = parser.extract_text(uploaded_file)

                st.write("Performing Semantic Analysis...")
                report = parser.analyze_content(text_data)
                
                # Extract initial queries
                queries = parser.get_search_queries(report)
                
                status.update(label="Agent A Analysis Complete!", state="complete", expanded=False)
                
            st.session_state['agent_a_report'] = report
            st.session_state['agent_a_queries'] = queries
            st.rerun()
        except Exception as e:
            st.error(f"Error during parsing: {e}")
            st.stop()

    # Display Agent A Findings and HitL Queries
    if 'agent_a_report' in st.session_state:
        st.divider()
        st.subheader("Agent A: Parser Report")
        st.markdown(st.session_state['agent_a_report'])
        st.success("Data ready for Agent B (The Scout)!")
        
        # HitL: Human in the Loop for Queries
        st.subheader("🛠️ Refine Search Queries (Optional)")
        st.write("Agent A generated these queries. You can edit them before Agent B searches the web.")
        
        # Form or text area to edit queries
        queries_text = "\n".join(st.session_state['agent_a_queries'])
        edited_queries_text = st.text_area("Research Queries (One per line)", value=queries_text, height=100)
        edited_queries = [q.strip() for q in edited_queries_text.split('\n') if q.strip()]

        if st.button("Let Agent B Scout 2026 Trends"):
            st.session_state['final_queries'] = edited_queries
            try:
                scout = AgentB_Scout(st.session_state['serper_api_key'])
                with st.spinner("Agent B is searching the live web..."):
                    web_data = scout.search_2026(st.session_state['final_queries'])
                    st.session_state['web_data'] = web_data
            except Exception as e:
                st.error(f"Error during web search: {e}")

    # Display Agent B Findings
    if 'web_data' in st.session_state:
        st.divider()
        st.subheader("Agent B: Real-Time Findings")
        for res in st.session_state['web_data']:
            st.write(f"**Query:** {res['query']}")
            for f in res['findings']:
                st.write(f"- {f}")

        # Final Audit Step
        if st.button("Run Final Audit (Agent C)"):
            try:
                auditor = AgentC_Auditor(st.session_state['google_api_key'])
                syllabus_info = st.session_state['agent_a_report']
                web_info = str(st.session_state['web_data'])
                
                with st.spinner("Agent C is auditing the curriculum gap..."):
                    final_report = auditor.generate_audit_report(syllabus_info, web_info)
                
                st.session_state['final_report'] = final_report
            except Exception as e:
                st.error(f"Error during final audit: {e}")

    # Display Agent C Report and Download
    if 'final_report' in st.session_state:
        st.divider()
        st.header("Final Modernization Report")
        st.markdown(st.session_state['final_report'])

        st.download_button(
            label="Download Report as Markdown",
            data=st.session_state['final_report'],
            file_name="final_modernization_report.md",
            mime="text/markdown"
        )
