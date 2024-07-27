# Streamlit Chat Interface with Bedrock Agent Integration

This project is a web-based chat interface developed with Streamlit, integrated with a Bedrock Agent for interactive conversation. It provides a user-friendly interface to interact with the Bedrock Agent, manage chat sessions, and customize the appearance of the chat interface.

## Features

- **Customizable Background**: Load and display a custom background image.
- **Session Management**: Start new chat sessions, and view and resume previous sessions.
- **Custom Styling**: Apply custom CSS for various UI elements including navbar, title, chat messages, and footer.
- **Dynamic Title**: Generate a dynamic title with alternating color patterns.
- **Chat Interface**: Display user and assistant messages in a styled chat interface.
- **Real-time Interaction**: Send user inputs to the Bedrock Agent and display the agent's responses.

## Getting Started

### Prerequisites

- Python 3.x
- Streamlit
- Bedrock Agent runtime (custom module)

### Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install the required Python packages:
bash
Copy code
pip install streamlit
Make sure to install the bedrock_agent_runtime custom module as well.
Set up the environment variables:
bash
Copy code
export BEDROCK_AGENT_ID=<your-bedrock-agent-id>
export BEDROCK_AGENT_ALIAS_ID=<your-bedrock-agent-alias-id>
export BEDROCK_AGENT_TEST_UI_TITLE=<your-ui-title>
export BEDROCK_AGENT_TEST_UI_ICON=<your-ui-icon-url>
Usage
Run the Streamlit app:
bash
Copy code
streamlit run app.py
Open the provided URL in your web browser to interact with the chat interface.
Configuration
Background Image: Update the image_path variable in app.py with the path to your local image file.
Navbar Image: Change the navbar_image_url variable to point to the desired image URL for the navbar.
Customization
CSS Styling: Modify the CSS rules within the <style> tag in app.py to adjust the appearance of the navbar, title, footer, chat messages, and other elements.
Title Colors: Adjust the colors used in the generate_alternating_title function to match your desired theme.
Notes
The bedrock_agent_runtime module is a custom module for invoking the Bedrock Agent. Ensure it's properly configured in your environment.
This project assumes you have basic familiarity with Streamlit and Python. If you encounter issues, consult the Streamlit documentation for additional guidance.