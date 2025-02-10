import streamlit as st
import re
import random

# Pre-defined set of words to exclude
pre_excluded_words = {
    "I", "you", "he", "she", "it", "we", "they", "me", "us", "him", "her", 
    "my", "your", "his", "our", "them", "their", "a", "g", "do", "don't", 
    "don", "t", "in", "on", "at", "by", "for", "with", "about", "against", 
    "between", "into", "through", "during", "before", "after", "above", 
    "below", "to", "from", "up", "down", "in", "out", "over", "under", "again", "further", "then", "once"
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

def main():
    st.title("Lyrics Input and Processing App")
    
    # User inputs lyrics
    lyrics_input = st.text_area("Enter lyrics:")
    
    # Slider for number of words to replace
    num_words_to_replace = st.slider("Select number of words to replace:", 1, 20, 10)
    
    # Toggle for "Advanced Options"
    advanced_options = st.checkbox("Advanced Options")
    
    if advanced_options:
        st.subheader("Pre-defined excluded words:")
        st.write(sorted(pre_excluded_words))
        
        st.subheader("Additional excluded words:")
        additional_excluded_words = st.text_area("Enter additional words separated by commas:")
        
        st.subheader("Words to delete from exclusion list:")
        deleting_excluded_words = st.text_area("Enter words to delete separated by commas:")
    else:
        additional_excluded_words = ""
        deleting_excluded_words = ""
    
    if st.button("Process Lyrics"):
        if lyrics_input:
            # Convert user-input additional and deleting words into lists
            additional_words = [word.strip() for word in additional_excluded_words.split(',') if word.strip()]
            deleting_words = [word.strip() for word in deleting_excluded_words.split(',') if word.strip()]
            
            # Define the final excluded words list
            final_excluded_words = pre_excluded_words.union(additional_words) - set(deleting_words)
            
            replaced_lyrics, replaced_words = replace_words_with_brackets(lyrics_input, final_excluded_words, num_words_to_replace)
            
            st.subheader("Processed Lyrics:")
            st.write(replaced_lyrics)
            
            st.subheader("Replaced Words:")
            for i, word in enumerate(replaced_words, 1):
                st.write(f"{i} : {word}")
        else:
            st.error("Please enter lyrics.")

if __name__ == "__main__":
    main()