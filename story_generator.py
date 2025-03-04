from transformers import pipeline

def generate_story(genre, character, style, length):
    """
    Generate a short or medium-length story using a GPT-2 model.
    """
    story_prompt = (
        f"Once upon a time in a {genre} world, there was a hero named {character}. "
        f"This is a {style.lower()} tale of their adventure."
    )
    
    generator = pipeline("text-generation", model="gpt2-medium")  # Using a larger model for better output
    max_length = 200 if length == "Short" else 400  # Adjusting length
    
    story = generator(story_prompt, max_length=max_length, num_return_sequences=1, temperature=0.8)[0]['generated_text']
    return story
