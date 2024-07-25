import json
import os
import uuid
import streamlit as st
from services import bedrock_agent_runtime  # Custom module for invoking Bedrock Agent

# Retrieve configuration from environment variables
agent_id = os.environ.get("BEDROCK_AGENT_ID")  # The unique ID of the Bedrock Agent
agent_alias_id = os.environ.get("BEDROCK_AGENT_ALIAS_ID")  # Alias ID for testing
ui_title = os.environ.get("BEDROCK_AGENT_TEST_UI_TITLE")  # UI title
ui_icon = os.environ.get("BEDROCK_AGENT_TEST_UI_ICON")  # UI icon

# URL of the image to display in the navbar
navbar_image_url = "https://www.bart.gov/themes/custom/bart/logo.svg"

# Update this URL to point to your .jpg file
background_image_url = "https://www.bart.gov/sites/default/files/banner-home-lg.jpg"  # Change to your .jpg file URL

def init_state():
    """
    Initialize the session state variables for a new session.
    """
    st.session_state.session_id = str(uuid.uuid4())  # Generate a unique session ID
    st.session_state.messages = []  # Initialize an empty list for storing chat messages
    # st.session_state.citations = []  # Initialize an empty list for storing citations
    st.session_state.trace = {}  # Initialize an empty dictionary for storing trace information

# Configure the page layout and settings
st.set_page_config(page_title=ui_title, page_icon=ui_icon, layout="wide")  # Set the page title, icon, and layout

# Add custom CSS for the black navbar, center title, and background image
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');  /* Import Roboto font */
    
    body {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        margin: 0;
        padding: 0;
        color: #fff;
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font to the body */
    }}
    .navbar {{
        background-color: #000;
        color: #fff;
        padding: 10px;
        text-align: center;
        font-size: 16px;
    }}
    .navbar img {{
        height: 50px;
    }}
    .title {{
        text-align: center;
        margin-top: 20px;
        color: #fff;
        font-size: 48px;
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font to the title */
    }}
    .title span {{
        display: inline-block;
    }}
    .title .light-blue {{
        color: #0099D8; 
    }}
    .title .black {{
        color: #000;
    }}
    .groot {{
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font specifically to GROOT */
        font-weight: 700;  /* Apply bold weight */
        font-size: 60px;  /* Adjust font size */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);  /* Add a subtle text shadow */
    }}
    </style>
    <div class="navbar">
        <img src="{navbar_image_url}" alt="BART Logo" />
    </div>
    """, unsafe_allow_html=True)

# Function to create the alternating color title
def generate_alternating_title(text):
    title_html = ""
    colors = ['black','light-blue']
    
    for i, char in enumerate(text):
        color_class = colors[i % len(colors)]  # Alternate colors
        title_html += f"<span class='{color_class}'>{char}</span>"
    
    return title_html

# Display the title at the top of the page
st.markdown(f"<h1 class='title groot'>{generate_alternating_title(ui_title)}</h1>", unsafe_allow_html=True)

# Initialize session state if not already initialized
if len(st.session_state.items()) == 0:
    init_state()  # Call the initialization function

# Sidebar for Reset Session and Memory Management
with st.sidebar:
    st.title("Previous Conversations")  # Display the title for the memory management section
    
    # Memory Tab
    # st.subheader("Memory")
    # Display previous messages in the conversation memory tab
    if st.session_state.messages:
        i = 0
        while i < len(st.session_state.messages):
            user_message = st.session_state.messages[i]
            assistant_message = st.session_state.messages[i + 1] if i + 1 < len(st.session_state.messages) else None

            # Use the user message content as the title of the expander
            expander_title = user_message['content'][:30] + '...' if len(user_message['content']) > 30 else user_message['content']
            
            with st.expander(f"Question: {expander_title}", expanded=False):
                # Display user message
                if user_message["role"] == "user":
                    st.markdown(f"**User:** {user_message['content']}", unsafe_allow_html=True)
                
                # Display assistant message
                if assistant_message and assistant_message["role"] == "assistant":
                    st.markdown(f"**Assistant:** {assistant_message['content']}", unsafe_allow_html=True)

                if st.button(f"Delete Conversation", key=f"delete_{i}"):
                    del st.session_state.messages[i:i + 2]  # Delete the user-assistant message pair
                    st.experimental_rerun()  # Refresh the app
            
            i += 2  # Increment by 2 to process the next pair of messages

    else:
        st.text("No messages in memory yet.")  # Indicate that there are no messages

    # Sidebar button to reset session state
    if st.button("Reset Session"):
        init_state()  # Reset the session state when the button is clicked
        st.experimental_rerun()  # Refresh the app

# Display previous messages in the conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Determine the role (user or assistant)
        st.markdown(message["content"], unsafe_allow_html=True)  # Display message content with markdown

# Capture user input and send it to the agent
if prompt := st.chat_input():
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat format
    with st.chat_message("user"):
        st.write(prompt)  # Show the user's input message

    # Placeholder for the assistant's response
    with st.chat_message("assistant"):
        placeholder = st.empty()  # Create an empty placeholder for the response
        placeholder.markdown("...")  # Display a loading indicator

        # Invoke the Bedrock agent with the user prompt
        response = bedrock_agent_runtime.invoke_agent(
            agent_id,
            agent_alias_id,
            st.session_state.session_id,
            prompt
        )

        output_text = response["output_text"]  # Retrieve the output text from the agent response

        # Update placeholder with the completed output text
        placeholder.markdown(output_text, unsafe_allow_html=True)

        # Append assistant's message to session state
        st.session_state.messages.append({"role": "assistant", "content": output_text})

        # Update session state with the new trace information
        st.session_state.trace = response["trace"]
