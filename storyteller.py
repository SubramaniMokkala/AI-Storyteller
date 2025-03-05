import streamlit as st
from transformers import pipeline

# Load a more advanced text generation model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

generator = load_model()

# Streamlit UI
st.title("📖 AI-Powered Storyteller (Enhanced Version)")
st.markdown("Enter a prompt, and the AI will generate a **well-structured** short story!")

# User input
prompt = st.text_area("Enter a story prompt (e.g., 'Once upon a time in a magical forest...')")

# Story length slider
length = st.slider("Story Length (words)", min_value=50, max_value=300, step=10, value=150)

# Generate button
if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating your story... ⏳"):
            story = generator(prompt, max_length=length, temperature=0.8, top_p=0.9, num_return_sequences=1)[0]["generated_text"]
            st.subheader("📝 Generated Story")
            st.write(story)
    else:
        st.warning("Please enter a prompt to generate a story!")

st.markdown("---")
st.caption("Powered by Hugging Face GPT-Neo | Free & Runs Locally 🚀")
