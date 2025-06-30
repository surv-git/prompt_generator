import streamlit as st
import json
import os
from streamlit_extras.stylable_container import stylable_container

# Configure page layout
st.set_page_config(page_title="Prompt Generator", layout="wide")

def load_config():
    """Load configuration from config.json file"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("config.json file not found!")
        return []
    except json.JSONDecodeError:
        st.error("Invalid JSON format in config.json!")
        return []

def refine_prompt():
    """Placeholder method for refine prompt functionality"""
    st.success("Refine Prompt button clicked! (Placeholder method)")

def send_prompt():
    """Placeholder method for send prompt functionality"""
    st.success("> Send button clicked! (Placeholder method)")

def main():
    st.title("Prompt Generator")
    
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"/>', unsafe_allow_html=True)

    # Load configuration data
    config_data = load_config()
    
    if not config_data:
        st.warning("No configuration data available.")
        return
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # 1. Farm selection
    farm_names = [item["farm"] for item in config_data]
    selected_farm = st.sidebar.selectbox("Select Farm:", farm_names)
    
    # Find selected farm data
    selected_farm_data = next((item for item in config_data if item["farm"] == selected_farm), None)
    
    if selected_farm_data:
        # 2. Method selection with radio buttons
        method_names = [method["name"] for method in selected_farm_data["method"]]
        selected_method = st.sidebar.radio("Select Method:", method_names)
        
        # Find selected method data
        selected_method_data = next((method for method in selected_farm_data["method"] if method["name"] == selected_method), None)
        
        if selected_method_data:
            # 3. MCP Agents with checkboxes
            st.sidebar.subheader("MCP Agents")
            selected_agents = []
            for agent in selected_method_data["mcp_agents"]:
                if st.sidebar.checkbox(agent["name"]):
                    selected_agents.append(agent["name"])
            
            # Main content area
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 4. System prompt textarea
                st.subheader("Prompt")
                
                # 5. Large textarea for system prompt (capable of handling ~256KB)
                system_prompt = st.text_area(
                    "Edit Prompt:",
                    value=selected_method_data["system_prompt"],
                    height=400,
                    max_chars=262144,  # 256KB limit
                    help="Maximum size: 256KB"
                )
                
                # 6. Buttons below textarea - right aligned
                col_spacer, col_btn1, col_btn2 = st.columns([5, 1, 1])
                
                with col_btn1:
                    with stylable_container(
                        key="refine_prompt_button",
                        css_styles=r"""
                            button p:before {
                            font-family: 'Font Awesome 5 Free';
                            content: '\f013';
                            display: inline-block;
                            padding-right: 10px;
                            vertical-align: middle;
                            font-weight: 900;
                        }
                        """,
                        ):
                        if st.button("Refine Prompt", type="secondary", use_container_width=True):
                            refine_prompt()
                
                with col_btn2:
                    with stylable_container(
                        key="send_button",
                        css_styles=r"""
                            button p:before {
                            font-family: 'Font Awesome 5 Free';
                            content: '\f1d8';
                            display: inline-block;
                            padding-right: 10px;
                            vertical-align: middle;
                            font-weight: 900;
                        }
                        """,
                        ):
                        if st.button("Send", type="primary", use_container_width=True):
                            send_prompt()
                
            with col2:
                # Display current selections with left padding using columns
                _, content_col = st.columns([0.1, 0.9], gap='large')
                with content_col:                    
                    st.subheader("Current Selection")
                    st.write(f"*Farm:* {selected_farm}")
                    st.write(f"*Method:* {selected_method}")
                    if selected_agents:
                        st.write(f"*Selected Agents:* {', '.join(selected_agents)}")
                    else:
                        st.write("*Selected Agents:* None")

if __name__ == "__main__":
    main()