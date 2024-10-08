import logging
import boto3
from botocore.exceptions import ClientError, EventStreamError
from botocore.config import Config
import time

# Set up logging to display debug information
logging.basicConfig(level=logging.DEBUG)

def invoke_agent(agent_id, agent_alias_id, session_id, prompt, max_retries=5):
    """
    Invokes an Amazon Bedrock agent to process a given prompt and returns the output, citations, and trace information.

    Parameters:
        agent_id (str): The unique identifier of the Bedrock agent to invoke.
        agent_alias_id (str): The alias ID of the Bedrock agent version to be used.
        session_id (str): A unique session identifier for tracking and managing the agent invocation.
        prompt (str): The input text or query to be processed by the agent.
        max_retries (int): The maximum number of retries for throttling errors.

    Returns:
        dict: A dictionary containing:
            - output_text (str): The concatenated output text generated by the agent.
            - citations (list): A list of citations related to the agent's output.
            - trace (dict): A dictionary containing trace information, including pre-processing, orchestration, and post-processing details.

    Raises:
        ClientError: If an error occurs while invoking the agent or communicating with the AWS service.
    """

    # Configure the retry logic
    config = Config(
        retries={
            'max_attempts': max_retries,
            'mode': 'adaptive'  # Uses adaptive retry mode
        }
    )

    try:
        # Create a client for the Bedrock Agent Runtime service using the default session
        client = boto3.session.Session().client(
            service_name="bedrock-agent-runtime",
            config=config
        )

        # Attempt to invoke the agent with exponential backoff for throttling
        retries = 0
        while retries < max_retries:
            try:
                # Invoke the Bedrock agent with the specified parameters
                response = client.invoke_agent(
                    agentId=agent_id,         # The unique identifier for the agent
                    agentAliasId=agent_alias_id,  # The alias ID of the agent's version to use
                    enableTrace=True,         # Enable tracing to get detailed processing information
                    sessionId=session_id,     # A unique identifier for this session
                    inputText=prompt,         # The prompt or query to be processed by the agent
                )
                
                # Initialize variables to store the output text, citations, and trace information
                output_text = ""


                # Process the completion events in the response
                for event in response.get("completion", []):
                    # Combine the chunks to get the output text
                    if "chunk" in event:
                        chunk = event["chunk"]
                        output_text += chunk["bytes"].decode()  # Concatenate the decoded bytes to the output text
                    
                # Return a dictionary with the output text, citations, and trace information
                return {
                    "output_text": output_text
                }

            except ClientError as e:
                # Check for throttling error
                if e.response['Error']['Code'] == 'ThrottlingException':
                    # Log the throttling event
                    logging.warning(f"Throttling error: {e}. Retrying in {2 ** retries} seconds...")
                    time.sleep(2 ** retries)  # Exponential backoff
                    retries += 1
                else:
                    # Log the error with a message
                    logging.error(f"An error occurred: {e}")
                    # Raise the error to signal that an exception has occurred
                    raise

            except EventStreamError as e:
                # Handle event stream errors separately
                logging.error(f"Event stream error: {e}")
                raise

            except Exception as e:
                # Handle other generic exceptions
                logging.error(f"An unexpected error occurred: {e}")
                raise

    # Handle any client errors that occur during the process
    except ClientError as e:
        # Log the error with a message
        logging.error(f"An error occurred: {e}")
        # Raise the error to signal that an exception has occurred
        raise
