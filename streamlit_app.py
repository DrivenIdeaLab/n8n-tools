import streamlit as st
import requests
import json
import base64
from io import StringIO

def magic_position_workflow(workflow):
    """Send workflow to magic positioning API and return the result"""
    try:
        response = requests.post(
            "https://api.ia2s.app/webhook/workflow/magic/position",
            json={"workflow": workflow},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def handle_file_upload():
    """Handle workflow upload through file"""
    uploaded_file = st.file_uploader("Or upload workflow file", type=['json'])
    if uploaded_file is not None:
        try:
            workflow_json = json.load(uploaded_file)
            return json.dumps(workflow_json)
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file")
            return None

def create_download_link(json_data, filename="positioned_workflow.json"):
    """Create a download link for the JSON data"""
    json_str = json.dumps(json_data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}" class="downloadButton">Download Positioned Workflow</a>'
    return href

def main():
    st.set_page_config(
        page_title="n8n Tools",
        page_icon="🔧",
        layout="wide",
    )

    # Custom CSS for better performance with large text
    st.markdown("""
        <style>
        .downloadButton {
            background-color: rgba(22, 40, 216, 0.5);  /* Deep red with 50% transparency */
            border: none;
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        .downloadButton:hover {
            background-color: rgba(22, 40, 216, 0.7);  /* Darker on hover */
        }
        .stTextArea textarea {
            font-family: monospace;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("n8n Tools")
    selected_tool = st.sidebar.radio(
        "Select Tool",
        ["Magic Workflow Positioning"]
    )

    # Main content area
    st.title("n8n Tools")

    if selected_tool == "Magic Workflow Positioning":
        st.header("Magic Workflow Positioning")
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input Workflow")
            status_container = st.empty()
            
            # Add file upload option
            workflow_text = handle_file_upload()
            
            # Text input with reduced height and monospace font
            if not workflow_text:
                workflow_text = st.text_area(
                    "Or paste your workflow here",
                    height=400,
                    help="Paste your n8n workflow JSON here",
                    key="workflow_input"
                )
            
            if workflow_text:
                try:
                    workflow_json = json.loads(workflow_text)
                    
                    # Only process if content has changed
                    if ('last_input' not in st.session_state or 
                        st.session_state.last_input != workflow_text):
                        
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            st.session_state.positioned_workflow = result
                            st.session_state.last_input = workflow_text
                            status_container.success("✅ Workflow positioned successfully!")
                        else:
                            status_container.error("❌ Positioning failed - API error")
                    
                except json.JSONDecodeError:
                    status_container.error("❌ Invalid JSON format")

        with col2:
            st.subheader("Positioned Workflow")
            if 'positioned_workflow' in st.session_state:
                # Add download button
                st.markdown(
                    create_download_link(st.session_state.positioned_workflow),
                    unsafe_allow_html=True
                )
                
                # Format the full workflow as JSON string
                formatted_workflow = json.dumps(st.session_state.positioned_workflow, indent=2)
                
                
                # Show preview or full workflow based on size
                if len(formatted_workflow) > 50000:
                    with st.expander("Show Full Workflow"):
                        st.code(formatted_workflow, language='json')
                        # Hidden div containing full workflow for copy functionality
                        st.markdown(f'<div id="fullWorkflow" style="display:none">{formatted_workflow}</div>', unsafe_allow_html=True)
                else:
                    st.code(formatted_workflow, language='json')
                    # Hidden div containing full workflow for copy functionality
                    st.markdown(f'<div id="fullWorkflow" style="display:none">{formatted_workflow}</div>', unsafe_allow_html=True)
                
            else:
                st.info("Paste a valid workflow JSON on the left to see the positioned result here.")

if __name__ == "__main__":
    main()
