import streamlit as st
from parsers import AgentA_Parser
from scout import AgentB_Scout
from auditor import AgentC_Auditor
import os
from google.api_core.exceptions import GoogleAPIError

# Constants
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# 1. Page Config.
st.set_page_config(page_title="Universal Syllabus Researcher", layout="wide")
st.title("Universal Syllabus Researcher")
st.write("Modernizing any curriculum using Multi-Agent AI (2026 Standards)")

@st.cache_data(show_spinner=False)
def get_cached_parser_analysis(_parser, text_data, _api_key):
    # Pass api key to make it recalculate on key change
    return _parser.analyze_content(text_data)

@st.cache_data(show_spinner=False)
def get_cached_scout_search(_scout, queries, _api_key):
    return _scout.search_2026(queries)

@st.cache_data(show_spinner=False)
def get_cached_audit_report(_auditor, syllabus_info, web_info, _api_key):
    return _auditor.generate_audit_report(syllabus_info, web_info)


def clear_session():
    # Clear session state when a new file is uploaded or reset is clicked
    for key in list(st.session_state.keys()):
        if key not in ['google_api_key', 'serper_api_key']:
            del st.session_state[key]

# 2. Side bar for instructions & Configuration
with st.sidebar:
    st.header("Configuration ⚙️")
    st.write("Provide your own API keys to use the application. Keys entered here will override environment variables.")
    
    # Try to get from environment first, offer input to override
    default_google_key = os.getenv("GOOGLE_API_KEY", "")
    default_serper_key = os.getenv("SERPER_API_KEY", "")

    google_api_key = st.text_input("Google Gemini API Key", value=default_google_key, type="password", help="Get this from Google AI Studio (https://aistudio.google.com/)")
    serper_api_key = st.text_input("Serper API Key", value=default_serper_key, type="password", help="Get this from serper.dev (https://serper.dev/)")
    
    st.session_state['google_api_key'] = google_api_key
    st.session_state['serper_api_key'] = serper_api_key

    if not google_api_key or not serper_api_key:
        st.warning("⚠️ Please provide both API keys to proceed.")

    st.markdown("---")
    st.header("How to Use")
    st.info("Upload any PDF or PPTX syllabus. Agent A will parse it and identify the subject automatically")
    
    if st.button("Reset Application"):
        clear_session()
        st.rerun()
        
    st.markdown("---")
    st.subheader("Privacy Policy & Terms")
    st.caption("By using this tool, you acknowledge that uploaded documents are temporarily processed by Google (Gemini) and Serper APIs for analysis and are not permanently stored by this application.")

# Stop execution if API keys are missing
if not st.session_state['google_api_key'] or not st.session_state['serper_api_key']:
    st.info("👈 Please enter your API keys in the sidebar to get started.")
    st.stop()

# 3. Legal Agreement
st.write("### Data Processing Agreement")
agree_to_terms = st.checkbox("I agree to the Terms of Service and understand that my uploaded documents will be processed by third-party AI APIs (Google Gemini, Serper.dev).")

if not agree_to_terms:
    st.warning("You must agree to the Terms of Service to upload and analyze your syllabus.")
    st.stop()

# 4. File uploader
st.info("💡 **Tip:** Don't have a syllabus right now? Try uploading a sample PDF to test the app!")
uploaded_file = st.file_uploader(f"Upload Syllabus (PDF or PPTX, Max {MAX_FILE_SIZE_MB}MB)", type=["pdf", "pptx"], on_change=clear_session)

if uploaded_file:
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        st.error(f"❌ File size exceeds {MAX_FILE_SIZE_MB}MB limit. Please upload a smaller file.")
        st.stop()

    # Agent A Processing
    if 'agent_a_report' not in st.session_state:
        try:
            parser = AgentA_Parser(st.session_state['google_api_key'])
            with st.status("Agent A is working...", expanded=True) as status:
                st.write("Reading file contents...")
                text_data = parser.extract_text(uploaded_file)
                
                if not text_data.strip():
                    status.update(label="Parsing failed!", state="error", expanded=True)
                    st.error("No extractable text found in the document. It might be scanned or image-based.")
                    st.stop()

                st.write("Performing Semantic Analysis...")
                report = get_cached_parser_analysis(parser, text_data, st.session_state['google_api_key'])
                
                # Extract initial queries
                queries = parser.get_search_queries(report)
                
                status.update(label="Agent A Analysis Complete!", state="complete", expanded=False)
                
            st.session_state['agent_a_report'] = report
            st.session_state['agent_a_queries'] = queries
            st.rerun()
        except GoogleAPIError as e:
            st.error(f"❌ Gemini API Error: Please check your API key or quota. Details: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ An unexpected error occurred during parsing: {e}")
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
        st.caption("ℹ️ **Tip:** Good queries are specific, include the year '2026', and focus on industry trends rather than basic definitions.")
        
        # Form or text area to edit queries
        queries_text = "\n".join(st.session_state['agent_a_queries'])
        edited_queries_text = st.text_area("Research Queries (One per line)", value=queries_text, height=100)
        edited_queries = [q.strip() for q in edited_queries_text.split('\n') if q.strip()]

        if st.button("Let Agent B Scout 2026 Trends"):
            st.session_state['final_queries'] = edited_queries
            try:
                scout = AgentB_Scout(st.session_state['serper_api_key'])
                with st.spinner("Agent B is searching the live web..."):
                    web_data = get_cached_scout_search(scout, st.session_state['final_queries'], st.session_state['serper_api_key'])
                    st.session_state['web_data'] = web_data
            except Exception as e:
                st.error(f"❌ Error during web search: {e}. Please check your Serper API Key.")

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
                    final_report = get_cached_audit_report(auditor, syllabus_info, web_info, st.session_state['google_api_key'])
                
                st.session_state['final_report'] = final_report
            except GoogleAPIError as e:
                st.error(f"❌ Gemini API Error during audit: {e}. Please check quota/key.")
            except Exception as e:
                st.error(f"❌ Unexpected error during final audit: {e}")

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
