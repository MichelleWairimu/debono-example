import os
from pathlib import Path
import gradio as gr
import asyncio
import pandas as pd
from asyncflows import AsyncFlows
from asyncflows.utils.async_utils import merge_iterators
from asyncflows.log_config import get_logger
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("REST_PASSWORD")

# Define a Pydantic model for validation
class ContextElement(BaseModel):
    query: str

# Function to log and print debug messages
def log_debug(message):
    print(message)  # Print to console
    get_logger().debug(message)  # Log to asyncflows logger

# Define the Gradio interface
with gr.Blocks() as demo:
    query = gr.Textbox(label="Problem", placeholder="Provide a problem to think about")
    submit_button = gr.Button("Submit")

    with gr.Row():
        my_hat = gr.Textbox(label="my_hat", interactive=False)
        white_hat = gr.Textbox(label="White Hat", interactive=False)
        red_hat = gr.Textbox(label="Red Hat", interactive=False)
        black_hat = gr.Textbox(label="Black Hat", interactive=False)
        yellow_hat = gr.Textbox(label="Yellow Hat", interactive=False)
        green_hat = gr.Textbox(label="Green Hat", interactive=False)
    blue_hat = gr.Textbox(label="Blue Hat (synthesis)", interactive=False)

    async def handle_submit(query):
        try:
            # Validate the input query using Pydantic
            log_debug(f"Received query: {query}")
            context_element = ContextElement(query=query)
            context_data = context_element.dict()
            log_debug(f"Validated context data: {context_data}")

            # Clear the output fields
            yield {
                my_hat: "",
                white_hat: "",
                red_hat: "",
                black_hat: "",
                yellow_hat: "",
                green_hat: "",
                blue_hat: "",
            }

            # Load the chatbot flow
            flow = AsyncFlows.from_file("debono.yaml").set_vars(
                query=context_data["query"],AUTH_TOKEN = token
            )
            log_debug("Flow loaded and variables set")

            log = get_logger()

            # Stream the hats
            async for hat, outputs in merge_iterators(
                log,
                [
                    my_hat,
                    white_hat,
                    red_hat,
                    black_hat,
                    yellow_hat,
                    green_hat
                ],
                [
                    flow.stream('my_hat.result'),
                    flow.stream('white_hat.result'),
                    flow.stream('red_hat.result'),
                    flow.stream('black_hat.result'),
                    flow.stream('yellow_hat.result'),
                    flow.stream('green_hat.result'),
                ],
            ):
                log_debug(f"Received output for {hat}: {outputs}")
                yield {
                    hat: outputs
                }

            # Stream the blue hat
            async for outputs in flow.stream("blue_hat.result"):
                log_debug(f"Received output for blue_hat: {outputs}")
                yield {
                    blue_hat: outputs
                }

        except ValidationError as e:
            error_message = f"Validation error: {e}"
            log_debug(error_message)
            yield {
                white_hat: error_message,
                my_hat:"",
                red_hat: "",
                black_hat: "",
                yellow_hat: "",
                green_hat: "",
                blue_hat: "",
            }
        except Exception as e:
            error_message = f"An error occurred: {e}"
            log_debug(error_message)
            yield {
                white_hat: error_message,
                my_hat:"",
                red_hat: "",
                black_hat: "",
                yellow_hat: "",
                green_hat: "",
                blue_hat: "",
            }

    submit_button.click(
        fn=handle_submit,
        inputs=[query],
        outputs=[
            white_hat,
            my_hat,
            red_hat,
            black_hat,
            yellow_hat,
            green_hat,
            blue_hat
        ],
    )

if __name__ == "__main__":
    demo.launch()
