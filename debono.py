from pydantic import BaseModel, ValidationError
from asyncflows import AsyncFlows
import asyncio
import structlog
from typing import Any  # Import Any from typing
import os
from dotenv import load_dotenv
import yaml

load_dotenv()
token = os.getenv("REST_PASSWORD")

# # Load YAML configuration
def load_config(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
'''            
# Load secret.yml
def load_secret(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

secrets = load_secret('secret.yml')

# Load debono.yaml
config = load_config('debono.yaml')

# Replace placeholders in config with actual values from secret.yml
if 'default_model' in config and 'auth_token' in config['default_model']:
    config['default_model']['auth_token'] = secrets['REST_PASSWORD']  # Using 'rest_password' from secret.yml
else:
    raise ValueError("Could not find 'auth_token' in debono.yaml or 'rest_password' in secret.yml.")
 '''           
# # Example usage
config = load_config('debono.yaml')

# Access environment variables
auth_token = os.getenv('AUTH_TOKEN')
'''
# Update your YAML config with the loaded environment variable
if auth_token:
    config['default_model']['auth_token'] = auth_token
else:
    raise ValueError("AUTH_TOKEN is not set in the environment variables.")
'''
# # Example usage
#print(config['default_model']['auth_token']['${REST_PASSWORD}'])

log = structlog.get_logger()

class QueryModel(BaseModel):
    query: str

class ContextElement(BaseModel):
    value: str
    heading: str

class TextDeclaration(BaseModel):
    text: str
    
    async def render(self, context: dict[str, Any]) -> str:
        # Simplified render method for demonstration
        return self.text

async def transform_from_config(self, log: structlog.stdlib.BoundLogger, context: dict[str, Any]) -> ContextElement:
    value = await self.render(context)
    heading = await TextDeclaration(text=self.heading).render(context)
    
    log.debug(f"Transforming from config: value={value}, heading={heading}")
    
    return ContextElement(
        value=value,
        heading=heading,
    )

async def main():
    try:
        # Get user input
        user_input = input("Provide a problem to think about: ")
        
        # Validate the input using Pydantic
        validated_input = QueryModel(query=user_input)
        
        # Proceed if validation is successful
        flow = AsyncFlows.from_file("debono.yaml").set_vars(
            query=validated_input.query,AUTH_TOKEN = token
        )

        # Mock the part of the asyncflows library to use our transform_from_config
        # This is a simplified example; the actual implementation will depend on how
        # asyncflows is structured.
        flow.transform_from_config = transform_from_config

        # Run the flow and return the default output (result of the blue hat)
        result = await flow.run()
        print(result)

    except ValidationError as exc:
        print(repr(exc.errors()[0]['type']))

if __name__ == "__main__":
    asyncio.run(main())
