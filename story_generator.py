from transformers import pipeline

class StoryGenerator:
    def __init__(self):
        # Initialize the text generation pipeline with a free model
        self.generator = pipeline('text-generation', 
                                 model='gpt2',
                                 max_length=1000)
    
    def generate_story(self, user_inputs):
        """Generate a story based on user parameters"""
        # Create a more structured prompt from user inputs
        prompt = self._create_improved_prompt(user_inputs)
        
        # Generate the story using the pipeline
        result = self.generator(prompt, 
                             max_length=1000, 
                             num_return_sequences=1,
                             temperature=0.7)
        
        # Extract the generated text
        generated_text = result[0]['generated_text']
        
        # Clean up the output (remove the prompt from the output)
        story = generated_text.replace(prompt, "").strip()
        
        # Additional post-processing to improve readability
        story = self._post_process_story(story)
        
        return story
    
    def _create_improved_prompt(self, inputs):
        """Create a more focused and detailed prompt"""
        genre = inputs.get("genre", "romance")
        characters = inputs.get("characters", [])
        setting = inputs.get("setting", "a romantic setting")
        plot_elements = inputs.get("plot_elements", [])
        tone = inputs.get("tone", "serious")
        
        # Create character descriptions
        char_descriptions = []
        for char in characters:
            char_descriptions.append(f"{char['name']}: {char['description']}")
        
        # Construct a more specific prompt
        prompt = f"""Write a {tone} {genre} story with the following elements:

Setting: {setting}

Characters:
{', '.join(char_descriptions) if char_descriptions else 'Two main characters'}

Plot Elements to Include:
{', '.join(plot_elements) if plot_elements else 'A romantic journey'}

Story Structure:
- Begin with an intriguing scene that introduces the main characters
- Develop the relationship between the characters
- Include tension or conflict
- Resolve the main plot points
- End with a meaningful conclusion

The story begins:
"""
        return prompt
    
    def _post_process_story(self, story):
        """Clean up and improve the generated story"""
        # Remove repetitive or nonsensical lines
        lines = story.split('\n')
        unique_lines = []
        seen_phrases = set()
        
        for line in lines:
            # Remove extremely short or redundant lines
            if len(line.strip()) < 5:
                continue
            
            # Remove repetitive content
            if line.strip() not in seen_phrases:
                unique_lines.append(line)
                seen_phrases.add(line.strip())
        
        # Rejoin the lines and do some basic formatting
        cleaned_story = '\n\n'.join(unique_lines)
        
        # Limit story length
        cleaned_story = ' '.join(cleaned_story.split()[:300])
        
        return cleaned_story