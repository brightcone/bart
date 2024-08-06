import base64
import streamlit as st
import os
from services import bedrock_agent_runtime  # Custom module for invoking Bedrock Agent
import uuid

ui_title = os.environ.get("BEDROCK_AGENT_TEST_UI_TITLE")  # UI title
ui_icon = os.environ.get("BEDROCK_AGENT_TEST_UI_ICON")  # UI icon

# Function to convert image to base64 string
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the page configuration
st.set_page_config(page_title=ui_title, page_icon=ui_icon, layout="wide")  # Set the page title, icon, and layout

# Load the local image
image_path = "/Users/aneeshbukya/Desktop/Projects/bart/web-UI/background-1920x1080.JPG"  # Update with the path to your local image
image_base64 = load_image(image_path)

background_image = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: linear-gradient(
        rgba(0, 0, 0, 0.5), 
        rgba(0, 0, 0, 0.5)
    ), url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;  /* Ensure the image covers the entire viewport */
    background-position: center;  
    background-repeat: no-repeat;
    background-color: #000;  /* Fallback color in case the image fails to load */
    min-height: 100vh;  /* Ensure the container takes at least the full viewport height */
}}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# URL of the image to display in the navbar
navbar_image_url = "https://www.bart.gov/themes/custom/bart/logo.svg"

def init_state():
    """
    Initialize the session state variables for a new session.
    """
    st.session_state.session_id = str(uuid.uuid4())  # Generate a unique session ID
    st.session_state.messages = []  # Initialize an empty list for storing chat messages
    st.session_state.trace = {}  # Initialize an empty dictionary for storing trace information
    st.session_state.IT_agent_active = False  # New flag to track laptop task mode
    st.session_state.password_reset_agent_active = False  # New flag to track VPN task mode
    st.session_state.email_agent_active = False  # New flag to track printer task mode
    
if len(st.session_state.items()) == 0:
    init_state()  # Call the initialization function

# Add custom CSS for the larger navbar and smaller GROOT title
# Add custom CSS for the footer and chat messages
# Add custom CSS for the larger navbar, title, footer, and chat messages
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');  /* Import Roboto font */
    
    body {{
        margin: 0;
        padding: 0;
        color: #000;  /* Default text color set to black */
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font to the body */
        padding-left: 240px;  /* Ensure there's space on the left for the fixed sidebar */
    }}
    .navbar {{
        background-color: #000;
        color: #fff;
        padding: 100px;  /* Increased padding for larger navbar */
        text-align: center;
        font-size: 30px;  /* Increased font size for the navbar */
        height: 150px;  /* Increased height for the navbar */
        display: flex;
        align-items: center;  /* Vertically center the content */
        justify-content: center;  /* Horizontally center the content */
        width: 100vw;  /* Ensure the navbar spans the full viewport width */
        position: fixed;  /* Fix the navbar to the viewport */
        top: 45px;  /* Align the navbar to the top of the viewport */
        left: 240px;  /* Align the navbar to the left edge */
        z-index: 1000;  /* Ensure it stays on top of other content */
    }}
    .navbar img {{
        height: 180px;  /* Increased logo size to match the larger navbar */
    }}
    .title {{
        text-align: center;
        margin-top: 95px;  /* Reduced margin-top to decrease the gap */
        color: #000;  /* Set title color to black */
        font-size: 36px;  /* Decreased font size for the title */
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font to the title */
    }}
    .title span {{
        display: inline-block;
        margin-right: 8px; /* Add space between each letter */
    }}
    .title .light-blue {{
        color: #0099D8; /* Use the preferred light blue color */
    }}
    .title .white {{
        color: #fff;  /* White title text color changed to black */
    }}
    .groot {{
        font-family: 'Times New Roman', serif;  /* Change font specifically to Times New Roman */
        font-weight: 700;  /* Apply bold weight */
        font-size: 60px;  /* Decreased font size */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);  /* Add a subtle text shadow */
    }}
    .chat-message.user {{
        display: inline-block;  /* Adjust width based on content */
        max-width: 80%;  /* Limit the maximum width */
        word-wrap: break-word;  /* Ensure long words break to fit within the container */
        font-size: 20px;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: black;
        text-align: right; /* Align user messages to the right */
        padding-right: 50px; /* Add padding to the right */
    }}
    .chat-message.assistant {{
        display: inline-block;  /* Adjust width based on content */
        max-width: 80%;  /* Limit the maximum width */
        word-wrap: break-word;  /* Ensure long words break to fit within the container */
        font-size: 20px;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
        background-color: #808080;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: black;
        text-align: left; /* Align assistant messages to the left */
    }}
    .sidebar-button {{
        display: block;
        width: 100%;
        text-align: left;
        padding: 10px;
        margin-bottom: 5px;
        background-color: #f5f5f5;  /* Light grey background */
        border: 1px solid #ddd;  /* Light border */
        border-radius: 5px;  /* Rounded corners */
        font-size: 16px;
        color: #333;  /* Dark text color */
    }}
    .sidebar-button:hover {{
        background-color: #e0e0e0;  /* Slightly darker grey on hover */
        cursor: pointer;
    }}
    .memory-section {{
        font-size: 20px;  /* Match the font size of chat messages */
        font-weight: 700;  /* Match the font weight of chat messages */
        font-family: 'Roboto', sans-serif;  /* Apply Roboto font to memory section */
        background-color: #fff;  /* Match the background color to chat messages */
        padding: 10px;  /* Padding inside memory blocks */
        border-radius: 8px;  /* Rounded corners */
        margin-bottom: 10px;  /* Space between memory blocks */
        color: #000;  /* Black text color for contrast */
    }}
    </style>
    <div class="navbar">
        <img src="{navbar_image_url}" alt="BART Logo" />
    </div>

    """, unsafe_allow_html=True)
# Create a sidebar
sidebar = st.sidebar

# Function to display previous sessions as clickable blocks with user input summary
def display_previous_sessions():
    if 'previous_sessions' in st.session_state:
        for session in st.session_state.previous_sessions:
            # Get the summary of the first user message
            first_message = next((msg['content'] for msg in session['messages'] if msg['role'] == 'user'), 'No user messages')
            message_summary = first_message[:50] + '...' if len(first_message) > 50 else first_message
            
            # Generate a unique key for each button
            button_key = f"session_{session['session_id']}"
            
            # Display button with the user input summary
            if sidebar.button(f"{message_summary}", key=button_key):
                # Load the selected session's messages
                st.session_state.messages = session['messages']
                st.session_state.session_id = session['session_id']


# Add a button to start a new session
if sidebar.button('Start New Session'):
    # Store the previous session's messages
    if 'session_id' in st.session_state:
        if 'previous_sessions' not in st.session_state:
            st.session_state.previous_sessions = []
        st.session_state.previous_sessions.append({
            'session_id': st.session_state.session_id,
            'messages': st.session_state.messages
        })

    # Start a new session
    init_state()

# Display the previous sessions in the sidebar as clickable blocks
display_previous_sessions()

# Function to create the title with specific color pattern for GROOT
def generate_alternating_title(text):
    if text == "GROOT":
        title_html = (
            "<span class='white'>G</span>"
            "<span class='white'>R</span>"
            "<span class='light-blue'>O</span>"
            "<span class='light-blue'>O</span>"
            "<span class='white'>T</span>"
        )
    else:
        title_html = ""
        colors = ['white', 'light-blue']
        
        for i, char in enumerate(text):
            color_class = colors[i % len(colors)]  # Alternate colors
            title_html += f"<span class='{color_class}'>{char}</span>"
    
    return title_html

# Display the title at the top of the page
st.markdown(f"<h1 class='title groot'>{generate_alternating_title(ui_title)}</h1>", unsafe_allow_html=True)

# Initialize session state if not already initialized
if len(st.session_state.items()) == 0:
    init_state()  # Call the initialization function

# Display the conversation
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        color_class = 'user' if message['role'] == 'user' else 'assistant'
        st.markdown(f"<div class='chat-message {color_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Capture user input and send it to the agent
prompt = st.chat_input()

# Check if prompt is not None before proceeding
if prompt is not None:
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat format
    with st.chat_message("user"):
        st.markdown(
            f"<div class='chat-message user'>{prompt}</div>", 
            unsafe_allow_html=True
        )  # Show the user's input message

    # Placeholder for the assistant's response
    with st.chat_message("assistant"):
        placeholder = st.empty()  # Create an empty placeholder for the response
        placeholder.markdown("...")  # Display a loading indicator

        # Retrieve configuration from environment variables
        agent_id_1 = os.environ.get("BEDROCK_AGENT_ID_1")  # The unique ID of the first Bedrock Agent
        agent_alias_id_1 = os.environ.get("BEDROCK_AGENT_ALIAS_ID_1")  # Alias ID for the first agent (testing)
        agent_id_2 = os.environ.get("BEDROCK_AGENT_ID_2")  # Unique ID for the second agent
        agent_alias_id_2 = os.environ.get("BEDROCK_AGENT_ALIAS_ID_2")  # Alias ID for the second agent (testing)
        agent_id_3 = os.environ.get("BEDROCK_AGENT_ID_3")  # Unique ID for the third agent
        agent_alias_id_3 = os.environ.get("BEDROCK_AGENT_ALIAS_ID_3")  # Alias ID for the third agent (testing)
        agent_id_4 = os.environ.get("BEDROCK_AGENT_ID_4")  # Unique ID for the fourth agent
        agent_alias_id_4 = os.environ.get("BEDROCK_AGENT_ALIAS_ID_4")  # Alias ID for the fourth agent (testing)

        # Conditional logic to choose the agent based on the user's input
        if "thanks" in prompt.lower() or "thank you" in prompt.lower():
            st.session_state.IT_agent_active = False
            st.session_state.password_reset_agent_active = False
            st.session_state.email_agent_active = False
            chosen_agent_id = agent_id_1
            chosen_agent_alias_id = agent_alias_id_1
            print("-------------------------------------SWITCHING BACK TO AGENT 1-------------------------------------")
        elif (
            st.session_state.IT_agent_active
            or "laptop" in prompt.lower()
            or "computer" in prompt.lower()
            or "vpn" in prompt.lower()
        ):
            chosen_agent_id = agent_id_2
            chosen_agent_alias_id = agent_alias_id_2
            st.session_state.IT_agent_active = True  # Set the flag to True once Agent 2 is activated
            print("-------------------------------------AGENT 2-------------------------------------")
        elif(
            st.session_state.password_reset_agent_active
            or "reset my password" in prompt.lower()
        ):
            chosen_agent_id = agent_id_3
            chosen_agent_alias_id = agent_alias_id_3
            st.session_state.password_reset_agent_active = True
            print("-------------------------------------AGENT 3-------------------------------------")  
        elif(
            st.session_state.email_agent_active
            or "send an email" in prompt.lower()
            or "draft an email" in prompt.lower()
        ):
            chosen_agent_id = agent_id_4
            chosen_agent_alias_id = agent_alias_id_4
            st.session_state.email_agent_active = True
            print("-------------------------------------AGENT 4-------------------------------------")            
        else:
            chosen_agent_id = agent_id_1
            chosen_agent_alias_id = agent_alias_id_1
            print("-------------------------------------------AGENT 1-------------------------------------------")

        # Invoke the Bedrock agent with the user prompt
        response = bedrock_agent_runtime.invoke_agent(
            chosen_agent_id,
            chosen_agent_alias_id,
            st.session_state.session_id,
            prompt
        )
        output_text = response["output_text"]  # Retrieve the output text from the agent response

        # Update placeholder with the completed output text
        placeholder.markdown(
            f"<div class='chat-message assistant'>{output_text}</div>", 
            unsafe_allow_html=True
        )

        # Append assistant's message to session state
        st.session_state.messages.append({"role": "assistant", "content": output_text})

