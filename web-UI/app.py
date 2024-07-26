import base64
import streamlit as st
import os
from services import bedrock_agent_runtime  # Custom module for invoking Bedrock Agent
import uuid

# Retrieve configuration from environment variables
agent_id = os.environ.get("BEDROCK_AGENT_ID")  # The unique ID of the Bedrock Agent
agent_alias_id = os.environ.get("BEDROCK_AGENT_ALIAS_ID")  # Alias ID for testing
ui_title = os.environ.get("BEDROCK_AGENT_TEST_UI_TITLE")  # UI title
ui_icon = os.environ.get("BEDROCK_AGENT_TEST_UI_ICON")  # UI icon

# Function to convert image to base64 string
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the page configuration
st.set_page_config(page_title=ui_title, page_icon=ui_icon, layout="wide")  # Set the page title, icon, and layout

# Load the local image
image_path = "/Users/aneeshbukya/Desktop/Projects/bart/web-UI/background.JPG"  # Update with the path to your local image
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

# Add custom CSS for the larger navbar and smaller GROOT title
# Add custom CSS for the footer and chat messages
# Add custom CSS for the larger navbar, title, footer, and chat messages
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
        width: 100%;  /* Ensure the navbar spans the full width */
        position: fixed;  /* Fix the navbar to the viewport */
        top: 45px;  /* Move the navbar to the top of the viewport */
        left: 240px;  /* Align the navbar to the left */
        z-index: 1000;  /* Ensure it stays on top of other content */
    }}
    .navbar img {{
        height: 180px;  /* Increased logo size to match the larger navbar */
    }}
    .title {{
        text-align: center;
        margin-top: 100px;  /* Reduced margin-top to decrease the gap */
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
    .footer {{
        background-color: #000;  /* Completely black background for the footer */
        color: #fff;  /* White text color */
        padding: 10px;  /* Adjusted padding for better spacing */
        text-align: center;  /* Center the text in the footer */
        position: fixed;  /* Fix the footer to the bottom of the viewport */
        bottom: 0;  /* Align the footer to the bottom */
        left: 240px;  /* Align the footer to the left to match the sidebar position */
        width: calc(100% - 240px);  /* Adjust width to account for the sidebar */
    }}
    .footer .footer-blue {{
        color: #0099D8;  /* Blue color for some elements in the footer */
    }}
    .chat-message.user {{
        display: inline-block;  /* Adjust width based on content */
        max-width: 80%;  /* Limit the maximum width */
        word-wrap: break-word;  /* Ensure long words break to fit within the container */
        font-size: 20px;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
        background-color: #d4d4d4;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #000;
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
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #000;
        text-align: left; /* Align assistant messages to the left */
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
    .sidebar {{
        position: fixed;  /* Fix the sidebar to the viewport */
        top: 0;  /* Align the sidebar to the top */
        left: 0;  /* Align the sidebar to the left */
        width: 240px;  /* Set the width of the sidebar */
        height: 100vh;  /* Make the sidebar full height */
        background-color: #f5f5f5;  /* Set the background color of the sidebar */
        overflow-y: auto;  /* Enable vertical scrolling if needed */
        padding: 20px;  /* Add padding inside the sidebar */
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);  /* Add a subtle shadow for depth */
    }}
    </style>
    <div class="navbar">
        <img src="{navbar_image_url}" alt="BART Logo" />
    </div>
    <div class="sidebar">
        <!-- Sidebar content here -->
    </div>
    <div class="footer">
        <p>Footer Content Here | <span class="footer-blue">Blue Accent</span></p>
    </div>
    """, unsafe_allow_html=True)



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

# Sidebar for Reset Session and Memory Management
with st.sidebar:
    st.title("Previous Conversations")  # Display the title for the memory management section
    
    # Memory Tab
    if st.session_state.messages:
        i = 0
        while i < len(st.session_state.messages):
            user_message = st.session_state.messages[i]
            assistant_message = st.session_state.messages[i + 1] if i + 1 < len(st.session_state.messages) else None

            # Use the user message content as the title of the expander
            expander_title = user_message['content'][:30] + '...' if len(user_message['content']) > 30 else user_message['content']
            
            with st.expander(f"{expander_title}", expanded=False):
                # Display user message
                if user_message["role"] == "user":
                    st.markdown(f"<div class='memory-section'>{user_message['content']}</div>", unsafe_allow_html=True)
                
                # Display assistant message
                if assistant_message and assistant_message["role"] == "assistant":
                    st.markdown(f"<div class='memory-section'>{assistant_message['content']}</div>", unsafe_allow_html=True)

                if st.button(f"Delete Conversation", key=f"delete_{i}"):
                    del st.session_state.messages[i:i + 2]  # Delete the user-assistant message pair
                    st.experimental_rerun()  # Refresh the app
            
            i += 2  # Increment by 2 to process the next pair of messages

    else:
        st.text("No messages in memory yet.")  # Indicate that there are no messages

# Display the conversation
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        color_class = 'user' if message['role'] == 'user' else 'assistant'
        st.markdown(f"<div class='chat-message {color_class}'>{message['content']}</div>", unsafe_allow_html=True)

# Capture user input and send it to the agent
if prompt := st.chat_input():
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat format
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-message user'>{prompt}</div>", unsafe_allow_html=True)  # Show the user's input message

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
        placeholder.markdown(f"<div class='chat-message assistant'>{output_text}</div>", unsafe_allow_html=True)

        # Append assistant's message to session state
        st.session_state.messages.append({"role": "assistant", "content": output_text})

        # Update session state with the new trace information
        st.session_state.trace = response["trace"]
