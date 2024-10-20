from openai import OpenAI
import os

class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.api_key = os.getenv("OPENAI_API_KEY")  # Make sure you set your API key as an environment variable
        self.client.api_key = self.api_key
        
        # Define paths for history storage
        self.history_file = "buffer/chat.txt"
        self.current_input_file = "buffer/chat_current_input.txt"
        
        # Ensure buffer directory exists
        os.makedirs("buffer", exist_ok=True)

    def generate_response(self, prompt):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}",
                    },
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def history_manager(self, keep_history: bool, short_or_long: int) -> str:
        """
        Generates a response based on user input with options for keeping history and controlling length.
        """
        # Clear the history if keep_history is False
        if not keep_history:
            with open(self.history_file, "w") as history_file:
                history_file.write("")  # Clear history by overwriting with an empty string

        # Load the existing conversation history
        history = ""
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as history_file:
                history = history_file.read()

        user_input = ""
        if os.path.exists(self.current_input_file):
            with open(self.current_input_file, "r") as current_input_file:
                user_input = current_input_file.read()

        # Define the system prompt for short or long responses
        system_prompt = "You are a computer scientist. Maintain context in conversations and provide informative responses."
        if short_or_long == 0:
            system_prompt += " Provide a concise and to-the-point response."
        else:
            system_prompt += " Provide a detailed and thorough response with explanations."

        # Create the complete prompt, including system instructions and conversation history
        prompt = f"{system_prompt}\n{history}User: {user_input}\nBot:"

        bot_response = self.generate_response(prompt)

        # Update the history with the current conversation
        updated_history = history + f"User: {user_input}\nBot: {bot_response}\n"
        # Limit the length of history to avoid overflow (adjustable based on context size)
        if len(updated_history) > 10000:
            updated_history = updated_history[-10000:]  # Keep only the last 10,000 characters of conversation

        # Write the updated history back to the file
        with open(self.history_file, "w") as history_file:
            history_file.write(updated_history)

        return bot_response



def response_generator(keep_history: bool, short_or_long: int):
    """
    Generates a chatbot response using OpenAI GPT-4 based on user input, with options to maintain conversation history and control response length.
    
    Args:
        keep_history (bool): 
            A flag that determines whether to maintain the conversation history across multiple interactions.
        short_or_long (int): 
            An integer flag that controls the length of the generated response:
            - `0` for a concise response.
            - `1` for a detailed and explanatory response.

    Returns:
        str: The generated chatbot response.
    """
    chatbot = ChatBot()
    return chatbot.history_manager(keep_history, short_or_long)
