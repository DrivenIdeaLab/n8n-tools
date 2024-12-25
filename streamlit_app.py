import streamlit as st
import requests
import json
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
    except requests.exceptions.RequestException:
        return None

def truncate_json_string(json_str, max_length=1000):
    """Return a truncated preview of a JSON string"""
    if len(json_str) <= max_length:
        return json_str
    return json_str[:max_length] + "..."

def main():
    st.set_page_config(
        page_title="n8n Tools",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0
    if 'preview_mode' not in st.session_state:
        st.session_state.preview_mode = True

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
            
            # Status messages container above the input
            status_container = st.empty()
            
            # Add file upload option
            uploaded_file = st.file_uploader(
                "Upload workflow JSON file",
                type=['json'],
                key=f"uploader_{st.session_state.file_uploader_key}"
            )

            # Toggle for preview mode
            st.session_state.preview_mode = st.checkbox(
                "Preview mode (recommended for large workflows)",
                value=st.session_state.preview_mode
            )

            if uploaded_file:
                try:
                    # Read the file content
                    workflow_str = uploaded_file.getvalue().decode()
                    workflow_json = json.loads(workflow_str)
                    
                    # Display preview or full content based on mode
                    if st.session_state.preview_mode:
                        st.text_area(
                            "Workflow preview (truncated)",
                            value=truncate_json_string(workflow_str),
                            height=200,
                            disabled=True
                        )
                    else:
                        st.text_area(
                            "Full workflow",
                            value=workflow_str,
                            height=600
                        )
                    
                    # Process workflow
                    if ('last_input' not in st.session_state or 
                        st.session_state.last_input != workflow_str):
                        
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            st.session_state.positioned_workflow = json.dumps(result, indent=2)
                            st.session_state.last_input = workflow_str
                            status_container.success("✅ Workflow positioned successfully!")
                        else:
                            status_container.error("❌ Positioning failed - API error")
                            
                except json.JSONDecodeError:
                    status_container.error("❌ Invalid JSON format")
            
            # Alternative manual input
            st.markdown("---")
            st.markdown("### Or paste workflow manually:")
            
            workflow_input = st.text_area(
                "Paste your workflow here",
                height=300,
                help="Paste your n8n workflow JSON here",
                key="workflow_input"
            )
            
            if workflow_input:
                try:
                    workflow_json = json.loads(workflow_input)
                    if ('last_manual_input' not in st.session_state or 
                        st.session_state.last_manual_input != workflow_input):
                        
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            st.session_state.positioned_workflow = json.dumps(result, indent=2)
                            st.session_state.last_manual_input = workflow_input
                            status_container.success("✅ Workflow positioned successfully!")
                        else:
                            status_container.error("❌ Positioning failed - API error")
                except json.JSONDecodeError:
                    status_container.error("❌ Invalid JSON format")

        with col2:
            st.subheader("Positioned Workflow")
            if 'positioned_workflow' in st.session_state:
                if st.session_state.preview_mode:
                    st.text_area(
                        "Preview of positioned workflow (truncated)",
                        value=truncate_json_string(st.session_state.positioned_workflow),
                        height=200,
                        disabled=True
                    )
                    # Download button for full result
                    st.download_button(
                        "Download full positioned workflow",
                        st.session_state.positioned_workflow,
                        file_name="positioned_workflow.json",
                        mime="application/json"
                    )
                else:
                    st.code(st.session_state.positioned_workflow, language='json')
                
                # Add copy button using JavaScript
                st.markdown("""
                    <button onclick="
                        navigator.clipboard.writeText(document.querySelector('pre code').textContent);
                        this.textContent='Copied!';
                        setTimeout(() => this.textContent='Copy to Clipboard', 2000);
                    " style="margin-top: 10px;">
                        Copy to Clipboard
                    </button>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.info("Paste a valid workflow JSON on the left to see the positioned result here.")

if __name__ == "__main__":
    main()import streamlit as st
import requests
import json
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
    except requests.exceptions.RequestException:
        return None

def truncate_json_string(json_str, max_length=1000):
    """Return a truncated preview of a JSON string"""
    if len(json_str) <= max_length:
        return json_str
    return json_str[:max_length] + "..."

def main():
    st.set_page_config(
        page_title="n8n Tools",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Initialize session state
    if 'file_uploader_key' not in st.session_state:
        st.session_state.file_uploader_key = 0
    if 'preview_mode' not in st.session_state:
        st.session_state.preview_mode = True

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
            
            # Status messages container above the input
            status_container = st.empty()
            
            # Add file upload option
            uploaded_file = st.file_uploader(
                "Upload workflow JSON file",
                type=['json'],
                key=f"uploader_{st.session_state.file_uploader_key}"
            )

            # Toggle for preview mode
            st.session_state.preview_mode = st.checkbox(
                "Preview mode (recommended for large workflows)",
                value=st.session_state.preview_mode
            )

            if uploaded_file:
                try:
                    # Read the file content
                    workflow_str = uploaded_file.getvalue().decode()
                    workflow_json = json.loads(workflow_str)
                    
                    # Display preview or full content based on mode
                    if st.session_state.preview_mode:
                        st.text_area(
                            "Workflow preview (truncated)",
                            value=truncate_json_string(workflow_str),
                            height=200,
                            disabled=True
                        )
                    else:
                        st.text_area(
                            "Full workflow",
                            value=workflow_str,
                            height=600
                        )
                    
                    # Process workflow
                    if ('last_input' not in st.session_state or 
                        st.session_state.last_input != workflow_str):
                        
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            st.session_state.positioned_workflow = json.dumps(result, indent=2)
                            st.session_state.last_input = workflow_str
                            status_container.success("✅ Workflow positioned successfully!")
                        else:
                            status_container.error("❌ Positioning failed - API error")
                            
                except json.JSONDecodeError:
                    status_container.error("❌ Invalid JSON format")
            
            # Alternative manual input
            st.markdown("---")
            st.markdown("### Or paste workflow manually:")
            
            workflow_input = st.text_area(
                "Paste your workflow here",
                height=300,
                help="Paste your n8n workflow JSON here",
                key="workflow_input"
            )
            
            if workflow_input:
                try:
                    workflow_json = json.loads(workflow_input)
                    if ('last_manual_input' not in st.session_state or 
                        st.session_state.last_manual_input != workflow_input):
                        
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            st.session_state.positioned_workflow = json.dumps(result, indent=2)
                            st.session_state.last_manual_input = workflow_input
                            status_container.success("✅ Workflow positioned successfully!")
                        else:
                            status_container.error("❌ Positioning failed - API error")
                except json.JSONDecodeError:
                    status_container.error("❌ Invalid JSON format")

        with col2:
            st.subheader("Positioned Workflow")
            if 'positioned_workflow' in st.session_state:
                if st.session_state.preview_mode:
                    st.text_area(
                        "Preview of positioned workflow (truncated)",
                        value=truncate_json_string(st.session_state.positioned_workflow),
                        height=200,
                        disabled=True
                    )
                    # Download button for full result
                    st.download_button(
                        "Download full positioned workflow",
                        st.session_state.positioned_workflow,
                        file_name="positioned_workflow.json",
                        mime="application/json"
                    )
                else:
                    st.code(st.session_state.positioned_workflow, language='json')
                
                # Add copy button using JavaScript
                st.markdown("""
                    <button onclick="
                        navigator.clipboard.writeText(document.querySelector('pre code').textContent);
                        this.textContent='Copied!';
                        setTimeout(() => this.textContent='Copy to Clipboard', 2000);
                    " style="margin-top: 10px;">
                        Copy to Clipboard
                    </button>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.info("Paste a valid workflow JSON on the left to see the positioned result here.")

if __name__ == "__main__":
    main()
