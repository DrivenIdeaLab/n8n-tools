import streamlit as st
import requests
import json

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
        st.error(f"Error communicating with the API: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="n8n Tools",
        page_icon="🔧",
        layout="wide",
    )

    # Sidebar for navigation
    st.sidebar.title("n8n Tools")
    selected_tool = st.sidebar.radio(
        "Select Tool",
        ["Magic Workflow Positioning"]  # Add more tools here as they're developed
    )

    # Main content area
    st.title("n8n Tools")

    if selected_tool == "Magic Workflow Positioning":
        st.header("Magic Workflow Positioning")
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input Workflow")
            workflow_input = st.text_area(
                "Paste your workflow here",
                height=600,
                help="Paste your n8n workflow JSON here"
            )
            
            if st.button("Position Workflow"):
                if workflow_input:
                    try:
                        # Parse input JSON to validate it
                        workflow_json = json.loads(workflow_input)
                        
                        # Send to API
                        result = magic_position_workflow(workflow_json)
                        
                        if result:
                            # Store the result in session state
                            st.session_state.positioned_workflow = json.dumps(result, indent=2)
                            st.success("Workflow positioned successfully!")
                        
                    except json.JSONDecodeError:
                        st.error("Invalid JSON input. Please check your workflow format.")
                else:
                    st.warning("Please paste a workflow first.")

        with col2:
            st.subheader("Positioned Workflow")
            if 'positioned_workflow' in st.session_state:
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
                st.info("Positioned workflow will appear here after processing.")

if __name__ == "__main__":
    main()
