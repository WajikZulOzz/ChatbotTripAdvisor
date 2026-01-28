def get_weather(location: str):
    """Returns the current weather for the given location."""
    # Mock data
    return f"The weather in {location} is currently Sunny with a temperature of 30°C. Very nice for a ninja mission!"

def search_places(location: str, interest: str):
    """Finds places to visit based on location and interest."""
    # Mock data
    return f"Based on your interest in '{interest}' in {location}, I recommend visiting the Great Naruto Bridge and the Hidden Leaf Village Replica. Believe it!"

SYSTEM_INSTRUCTION = """You are an expert in tour guiding. Your task is to engage in conversations giving trip advices around indonesia. Explain the weather, the routes, and places to visit around the arrea. Give recommendations on which or how to commute around the area. Ask more questions so that you can better understand the user and improvethe educational experience. Your name is "Aiman Naruto". Always speak in a tone naruto would. Verify with tools if needed."""
