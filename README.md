# GROOT - The BART's AI Helpdesk

This project is a web-based chat interface developed with Streamlit, integrated with a Bedrock Agent for interactive conversation. It provides a user-friendly interface to interact with the Bedrock Agent, manage chat sessions, and customize the appearance of the chat interface.

## Features

- **Customizable Background**: Load and display a custom background image.
- **Session Management**: Start new chat sessions, view, and resume previous sessions.
- **Custom Styling**: Apply custom CSS for various UI elements including navbar, title, chat messages, and footer.
- **Dynamic Title**: Generate a dynamic title with alternating color patterns.
- **Chat Interface**: Display user and assistant messages in a styled chat interface.
- **Real-time Interaction**: Send user inputs to the Bedrock Agent and display the agent's responses.

# Bart AI Agent LLM Architecture

![LLM Architecture to handle ai agents at scale](https://github.com/user-attachments/assets/a37edbe9-9cf2-444f-8847-a691f369cfe2)

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
    ```

2. Install the required Python packages:

    ```bash
    pip install streamlit
    ```

    Make sure to install the `bedrock_agent_runtime` custom module as well.

3. Set up the environment variables:

    ```bash
    export BEDROCK_AGENT_ID=<your-bedrock-agent-id>
    export BEDROCK_AGENT_ALIAS_ID=<your-bedrock-agent-alias-id>
    export BEDROCK_AGENT_TEST_UI_TITLE=<your-ui-title>
    export BEDROCK_AGENT_TEST_UI_ICON=<your-ui-icon-url>
    ```

### Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Notes

The bedrock_agent_runtime module is a custom module for invoking the Bedrock Agent. Ensure it's properly configured in your environment.
This project assumes you have basic familiarity with Streamlit and Python. If you encounter issues, consult the Streamlit documentation for additional guidance.
