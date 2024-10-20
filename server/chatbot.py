from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import os

class ChatBot:
    def __init__(self):
        model_name = "meta-llama/Llama-3.2-1B-Instruct"
        
        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load the model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            offload_folder="offload"
        )
        
        # Initialize the pipeline for text generation
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        
        # Define paths for history storage
        self.history_file = "buffer/chat.txt"
        self.current_input_file = "buffer/chat_current_input.txt"
        
        # Ensure buffer directory exists
        os.makedirs("buffer", exist_ok=True)

    def history_manager(self, keep_history: bool, short_or_long: int) -> str:
        """
        Generates a response based on user input with options for keeping history and controlling length.
        
        Args:
        keep_history (bool): Whether to keep conversation history.
        short_or_long (int): Whether to generate a short (0) or long (1) response.
        
        Returns:
        str: The chatbot's response.
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

        # Generate the response
        response = self.pipe(prompt, max_new_tokens=2048, num_return_sequences=1, use_cache=True)

        # Extract the response text after "Bot:"
        bot_response = response[0]['generated_text'].split("Bot:")[-1].strip()

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
    Generates a chatbot response based on user input, with options to maintain conversation history and control the response length.
    
    This function initializes a new instance of the `ChatBot` class and utilizes the `history_manager` method to handle the 
    conversation flow. It manages conversation history, reads user input from a predefined file (`buffer/chat_current_input.txt`), 
    and appends the user input to a history file (`buffer/chat.txt`). The chatbot then processes the user input with context (if enabled)
    and generates a response using a pre-trained language model.

    Args:
        keep_history (bool): 
            A flag that determines whether to maintain the conversation history across multiple interactions.
            - If `True`, the conversation history from the file (`buffer/chat.txt`) is retained and the current response will be appended to it.
            - If `False`, the conversation history is cleared before generating a new response, effectively starting a new chat session.
        
        short_or_long (int): 
            An integer flag that controls the length of the generated response:
            - `0` for a concise response.
            - `1` for a detailed and explanatory response.

    Returns:
        str: 
            The generated chatbot response based on the current user input, which is read from the file `buffer/chat_current_input.txt`.

    Example:
        >>> response = response_generator(keep_history=True, short_or_long=0)
        >>> print(response)
        'The capital of France is Paris.'
        
        In this example, the chatbot generates a concise response about the capital of France and retains the conversation history
        for future interactions.

    Notes:
        - This function assumes that the user input is always provided via the file `buffer/chat_current_input.txt`.
        - Conversation history is maintained in `buffer/chat.txt`, allowing the chatbot to preserve context between interactions.
        - Make sure to manually update the user input in `buffer/chat_current_input.txt` before calling the function for new inputs.
    """
    chatbot = ChatBot()
    return chatbot.history_manager(keep_history, short_or_long)
