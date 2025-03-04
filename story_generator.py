from transformers import pipeline

class StoryGenerator:
    def __init__(self):
        # Initialize the text generation pipeline with a free model
        # Using a smaller model for faster local generation
        self.generator = pipeline('text-generation', 
                                 model='gpt2',
                                 max_length=1000)
    
    def generate_story(self, user_inputs):
        """Generate a story based on user parameters"""
        # Create a prompt from user inputs
        prompt = self._create_prompt(user_inputs)
        
        # Generate the story using the pipeline
        result = self.generator(prompt, 
                             max_length=1000, 
                             num_return_sequences=1,
                             temperature=0.7)
        
        # Extract the generated text
        generated_text = result[0]['generated_text']
        
        # Clean up the output (remove the prompt from the output)
        story = generated_text.replace(prompt, "").strip()
        
        return story
    
    def _create_prompt(self, inputs):
        """Format user inputs into a story generation prompt"""
        # Extract parameters with defaults if not provided
        genre = inputs.get("genre", "fantasy")
        characters = inputs.get("characters", [])
        setting = inputs.get("setting", "a medieval kingdom")
        plot = inputs.get("plot_elements", [])
        tone = inputs.get("tone", "adventurous")
        
        # Format character information
        char_descriptions = []
        for char in characters:
            char_descriptions.append(f"{char['name']}: {char['description']}")
        characters_text = "\n".join(char_descriptions) if char_descriptions else "A mysterious protagonist"
        
        # Format plot elements
        plot_text = "\n".join([f"- {element}" for element in plot]) if plot else "A journey of self-discovery"
        
        # Construct the prompt (shorter for GPT-2 model limitations)
        prompt = f"""Write a {genre} story with these elements:
Setting: {setting}
Characters: {characters_text}
Plot: {plot_text}
Tone: {tone}

The story begins:
"""
        
        return prompt