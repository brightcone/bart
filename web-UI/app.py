import json
import os
import uuid
import streamlit as st
from services import bedrock_agent_runtime  # Custom module for invoking Bedrock Agent

# Retrieve configuration from environment variables
agent_id = os.environ.get("BEDROCK_AGENT_ID")  # The unique ID of the Bedrock Agent
agent_alias_id = os.environ.get("BEDROCK_AGENT_ALIAS_ID", "TSTALIASID")  # Alias ID for testing
ui_title = os.environ.get("BEDROCK_AGENT_TEST_UI_TITLE", "Agents for Amazon Bedrock Test UI")  # UI title
ui_icon = os.environ.get("BEDROCK_AGENT_TEST_UI_ICON")  # UI icon

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
st.title(ui_title)  # Display the title at the top of the page

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

# Headers for trace types used in the sidebar
# trace_type_headers = {
#     "preProcessingTrace": "Pre-Processing",  # Pre-processing phase
#     "orchestrationTrace": "Orchestration",  # Orchestration phase
#     "postProcessingTrace": "Post-Processing"  # Post-processing phase
# }

# Trace information types to display
# trace_info_types = ["invocationInput", "modelInvocationInput", "modelInvocationOutput", "observation", "rationale"]

# Sidebar section for trace information
# with st.sidebar:
#     st.title("Trace")  # Display the title for the trace section

#     # Show each trace type in separate sections
#     step_num = 1  # Initialize step number for trace steps
#     for trace_type in trace_type_headers:
#         st.subheader(trace_type_headers[trace_type])  # Display subheader for each trace type

#         # Check if the trace type is available in the session state
#         if trace_type in st.session_state.trace:
#             trace_steps = {}  # Initialize a dictionary to store trace steps

#             # Organize traces by step, similar to how it is shown in the Bedrock console
#             for trace in st.session_state.trace[trace_type]:
#                 # Iterate over each trace information type
#                 for trace_info_type in trace_info_types:
#                     if trace_info_type in trace:
#                         trace_id = trace[trace_info_type]["traceId"]  # Get the trace ID
                        
#                         # Append trace to the corresponding trace step
#                         if trace_id not in trace_steps:
#                             trace_steps[trace_id] = [trace]
#                         else:
#                             trace_steps[trace_id].append(trace)
#                         break  # Stop after finding the first relevant trace_info_type

#             # Display trace steps in JSON format similar to the Bedrock console
#             for trace_id in trace_steps.keys():
#                 with st.expander("Trace Step " + str(step_num), expanded=False):  # Create an expander for each trace step
#                     for trace in trace_steps[trace_id]:
#                         trace_str = json.dumps(trace, indent=2)  # Convert trace to JSON string with indentation
#                         st.code(trace_str, language="json", line_numbers=trace_str.count("\n"))  # Display trace as JSON code
#                 step_num += 1  # Increment step number
#         else:
#             st.text("None")  # Indicate that there are no traces available for this trace type

#     # # Display citations section in the sidebar
#     # st.subheader("Citations")  # Subheader for citations

#     # # Check if any citations are available
#     # if len(st.session_state.citations) > 0:
#     #     citation_num = 1  # Initialize citation number

#     #     # Iterate over citations and display each one
#     #     for citation in st.session_state.citations:
#     #         for retrieved_ref_num, retrieved_ref in enumerate(citation["retrievedReferences"]):
#     #             with st.expander("Citation [" + str(citation_num) + "]", expanded=False):  # Expander for each citation
#     #                 citation_str = json.dumps({
#     #                     "generatedResponsePart": citation["generatedResponsePart"],  # Citation generated response part
#     #                     "retrievedReference": citation["retrievedReferences"][retrieved_ref_num]  # Citation retrieved reference
#     #                 }, indent=2)
#     #                 st.code(citation_str, language="json", line_numbers=trace_str.count("\n"))  # Display citation as JSON code
#     #             citation_num += 1  # Increment citation number
#     # else:
#     #     st.text("None")  # Indicate that there are no citations available



    # st.session_state.citations = []  # Initialize an empty list for storing citations

# Questions 
# what are the features of JIRA
# what is bluejeans 
# what is the covid policy 
# how to record a zoom meeting
# How to Add a File to Your Windows Favorites List
# what is the cost of slack
# What is the number for employee verification?
# what is the lost and found policy
# what are the employee perks 
# how to download chrome




