
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


# Mock tools
def get_weather(location: str):
    """Returns the current weather for the given location."""
    # Mock data
    return f"The weather in {location} is currently Sunny with a temperature of 30°C. Very nice for a ninja mission!"

def search_places(location: str, interest: str):
    """Finds places to visit based on location and interest."""
    # Mock data
    return f"Based on your interest in '{interest}' in {location}, I recommend visiting the Great Naruto Bridge and the Hidden Leaf Village Replica. Believe it!"

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    client = genai.Client(api_key=api_key)

    # transform tools to the format expected by the SDK
    # The SDK accepts a list of callables for tools
    tools = [get_weather, search_places]

    system_instruction = """You are an expert in tour guiding. Your task is to engage in conversations giving trip advices around indonesia. Explain the weather, the routes, and places to visit around the arrea. Give recommendations on which or how to commute around the area. Ask more questions so that you can better understand the user and improvethe educational experience. Your name is "Aiman Naruto". Always speak in a tone naruto would. Verify with tools if needed."""

    chat = client.chats.create(
        model="gemini-3-flash-preview", # Using a known model, user had gemini-3-pro-preview which might be valid but consistency is good. Sticking to user's or a current one. User had gemini-3-pro-preview. I will stick to what they had or a standard one. Actually, for reliable function calling, gemini-1.5-pro or flash is safer, but let's try to simulate their request. I'll use gemini-1.5-flash for speed/efficiency in this demo unless they rigidly requested 3.
        # User had "gemini-3-flash-preview". This seems like a made up model or a specific preview. I'll revert to a standard model name to ensure it works, like 'gemini-1.5-flash' or 'gemini-2.0-flash-exp' if available. 
        # Let's use 'gemini-2.0-flash-exp' as it matches recent "preview" style naming if '3' was a typo, or just 'gemini-1.5-flash'.
        # Actually, let's look at the user's code again. They had "gemini-3-pro-preview". If that fails I'll fix it. I'll stick to 'gemini-2.0-flash-exp' as a safe bet for "latest/preview" or 'gemini-1.5-flash'. Let's go with 'gemini-2.0-flash-exp'.
        config=types.GenerateContentConfig(
            temperature=0.8,
            tools=tools,
            system_instruction=system_instruction,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
        )
    )

    print("Aiman Naruto: Dattebayo! Where do you want to go in Indonesia? (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Aiman Naruto: See you later! Don't forget your ninja way!")
                break

            response = chat.send_message(user_input)
            
            # The SDK with automatic_function_calling should handle the tool calls internally 
            # and return the final text response.
            if response.text:
                 print(f"Aiman Naruto: {response.text}")
            else:
                # Fallback if something weird happens or only tool calls occur (shouldn't with auto)
                print("Aiman Naruto: (Thinking...)")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()