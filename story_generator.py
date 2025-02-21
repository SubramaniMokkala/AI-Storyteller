from transformers import pipeline
import torch
import re

class StoryGenerator:
    def __init__(self):
        """Initialize the text generation model."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Using a better model than GPT-2
        self.generator = pipeline(
            'text-generation', 
            model='EleutherAI/gpt-neo-1.3B', 
            device=0 if device == "cuda" else -1
        )

    def generate_story(self, user_inputs):
        """Generate a story based on user-provided parameters."""
        prompt = self._create_prompt(user_inputs)
        
        # Generate text with improved settings
        result = self.generator(
            prompt, 
            max_length=400, 
            num_return_sequences=1, 
            temperature=0.9, 
            top_k=50, 
            top_p=0.95
        )
        
        # Extract generated text
        generated_text = result[0]['generated_text']
        
        # Remove repeated sentences
        story = self._remove_repeated_sentences(generated_text.replace(prompt, "").strip())
        
        return story

    def _create_prompt(self, inputs):
        """Format user inputs into a prompt for story generation."""
        genre = inputs.get("genre", "fantasy")
        setting = inputs.get("setting", "a medieval kingdom")
        tone = inputs.get("tone", "adventurous")

        # Process characters
        characters = inputs.get("characters", [])
        char_descriptions = [f"{char['name']}: {char['description']}" for char in characters]
        characters_text = "\n".join(char_descriptions) if char_descriptions else "A mysterious protagonist"

        # Process plot elements
        plot = inputs.get("plot_elements", [])
        plot_text = "\n".join([f"- {element}" for element in plot]) if plot else "A journey of self-discovery"

        # Construct the prompt
        prompt = f"""Write a {genre} story with these elements:
Setting: {setting}
Characters: {characters_text}
Plot: {plot_text}
Tone: {tone}

The story begins:
"""

        return prompt

    def _remove_repeated_sentences(self, text):
        """Remove repetitive sentences from generated text."""
        sentences = text.split(". ")
        seen = set()
        new_text = []
        
        for sentence in sentences:
            cleaned_sentence = re.sub(r"\W+", "", sentence.lower())  # Normalize sentence
            if cleaned_sentence not in seen:
                seen.add(cleaned_sentence)
                new_text.append(sentence)
        
        return ". ".join(new_text)
