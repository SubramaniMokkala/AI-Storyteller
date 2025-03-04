from transformers import pipeline

def generate_story(genre, character, style, length):
    """
    Generate a short or medium-length story using a GPT-2 model.
    """
    story_prompt = f"Write a {style} {genre} story featuring {character}."
    
    generator = pipeline("text-generation", model="gpt2")
    max_length = 150 if length == "Short" else 300  # Adjust length based on user choice
    
    story = generator(story_prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
    return story
