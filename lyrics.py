import streamlit as st
import re
import random

# Pre-defined set of words to exclude
pre_excluded_words = {
    "I", "you", "he", "she", "it", "we", "they", "me", "us", "him", "her", 
    "my", "your", "his", "our", "them", "their", "a", "g", "do", "don't", 
    "don", "t", "in", "on", "at", "by", "for", "with", "about", "against", 
    "between", "into", "through", "during", "before", "after", "above", 
    "below", "to", "from", "up", "down", "in", "out", "over", "under", "again", "further", "then", "once",
    "is", "will", "be", "was", "were", "am", "are", "has", "have", "had", "not"
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
    st.title("Lyrics Replacement App")
    
    # User input for lyrics
    lyrics = st.text_area("Enter lyrics:", height=300)
    
    # Slider for number of words to replace
    num_words_to_replace = st.slider("Select number of words to replace:", 1, 20, 10)
    
    if st.button("Process Lyrics"):
        if lyrics:
            replaced_lyrics, replaced_words = replace_words_with_brackets(lyrics, pre_excluded_words, num_words_to_replace)
            
            st.subheader("Processed Lyrics:")
            st.text_area("", replaced_lyrics, height=300)
            
            st.subheader("Replaced Words:")
            for i, word in enumerate(replaced_words, 1):
                st.write(f"{i} : {word}")
        else:
            st.error("Please enter lyrics.")

if __name__ == "__main__":
    main()
