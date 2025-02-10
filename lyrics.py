import streamlit as st
import re
import random
from fpdf import FPDF

# Pre-defined set of words to exclude
pre_excluded_words = {
    "I", "you", "he", "she", "it", "we", "they", "me", "us", "him", "her", 
    "my", "your", "his", "our", "them", "their", "a", "g", "do", "don't", 
    "don", "t", "in", "on", "at", "by", "for", "with", "about", "against", 
    "between", "into", "through", "during", "before", "after", "above", 
    "below", "to", "from", "up", "down", "in", "out", "over", "under", "again", "further", "then", "once",
    "is", "will", "be", "was", "were", "am", "are", "has", "have", "had", "not", "an", "the", "this", "that"
}

def replace_words_with_brackets(lyrics, excluded_words, num_words_to_replace):
    # Split lyrics into words
    words = re.findall(r'\b\w+\b', lyrics)
    # Exclude specific words
    exclude_words = set(excluded_words)
    # Randomly select specified number of words
    words_to_replace = set(random.sample([word for word in words if word not in exclude_words], min(num_words_to_replace, len(words))))
    # Create dictionary to replace words
    replacement_dict = {}
    replaced_words = []
    index = 1
    for word in words:
        if word in words_to_replace and word not in replacement_dict:
            replacement_dict[word] = f"[{index}]"
            replaced_words.append(word)
            index += 1
    # Replace words in lyrics
    replaced_lyrics = re.sub(r'\b\w+\b', lambda match: replacement_dict.get(match.group(0), match.group(0)), lyrics)
    return replaced_lyrics, replaced_words

def generate_pdf(lyrics):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, lyrics)
    return pdf

def main():
    st.title("Lyrics Replacement App")
    
    # User input for lyrics
    lyrics = st.text_area("Enter lyrics:", height=400)
    
    # Slider for number of words to replace
    num_words_to_replace = st.slider("Select number of words to replace:", 1, 20, 10)
    
    # Toggle for "Advanced Options"
    advanced_options = st.checkbox("Advanced Options")
    
    if advanced_options:
        st.subheader("Pre-defined excluded words:")
        st.write(", ".join(sorted(pre_excluded_words)))
        
        st.subheader("Additional excluded words:")
        additional_excluded_words = st.text_area("Enter additional words separated by commas:")
        
        st.subheader("Words to delete from exclusion list:")
        deleting_excluded_words = st.text_area("Enter words to delete separated by commas:")
        
        # Convert user input into lists
        additional_words = {word.strip() for word in additional_excluded_words.split(',') if word.strip()}
        deleting_words = {word.strip() for word in deleting_excluded_words.split(',') if word.strip()}
        
        # Define the final excluded words list
        final_excluded_words = pre_excluded_words.union(additional_words) - deleting_words
    else:
        final_excluded_words = pre_excluded_words
    
    if st.button("Process Lyrics"):
        if lyrics:
            replaced_lyrics, replaced_words = replace_words_with_brackets(lyrics, final_excluded_words, num_words_to_replace)
            
            st.subheader("Processed Lyrics:")
            st.text_area("", replaced_lyrics, height=400)
            
            st.subheader("Replaced Words:")
            st.write(", ".join(f"{i}: {word}" for i, word in enumerate(replaced_words, 1)))
            
            pdf = generate_pdf(replaced_lyrics)
            pdf_output = "processed_lyrics.pdf"
            pdf.output(pdf_output)
            with open(pdf_output, "rb") as file:
                st.download_button("Download PDF", file, file_name="processed_lyrics.pdf", mime="application/pdf")
        else:
            st.error("Please enter lyrics.")

if __name__ == "__main__":
    main()
