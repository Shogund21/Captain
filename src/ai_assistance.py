import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


class AIAssistant:
    def __init__(self, model_name='gpt-4'):
        self.model = ChatOpenAI(model=model_name, api_key=openai_api_key)
        self.context_manager = ContextManager()

    def get_response(self, prompt):
        try:
            # Combine prompt with context
            context = self.context_manager.get_context()
            full_prompt = self._build_prompt_with_context(prompt, context)
            print(f"Full Prompt: {full_prompt}")

            # Get response from the model
            response = self.model.invoke([{"role": "user", "content": full_prompt}])
            print(f"Raw Response: {response}")
            print(f"Response Type: {type(response)}")

            # Extract the content from the response
            content = response.content

            # Update context with new interaction
            self.context_manager.update_context('last_interaction', {
                'prompt': prompt,
                'response': content
            })

            return content
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred while processing the request."

    def _build_prompt_with_context(self, prompt, context):
        # Here you can define how to incorporate context into the prompt
        context_str = "\n".join([f"{key}: {value}" for key, value in context.items()])
        return f"{context_str}\n\nUser: {prompt}\nAI:"


class ContextManager:
    def __init__(self):
        self.context = {}

    def update_context(self, key, value):
        self.context[key] = value

    def get_context(self):
        return self.context
