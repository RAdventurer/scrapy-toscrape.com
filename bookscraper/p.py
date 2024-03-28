def sii(star_text: str):
    stars_mapping = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    # Split the input text by whitespace and punctuation
    words = star_text.split()
    
    # Search for words representing star ratings in the text
    for word in words:
        if word in stars_mapping:
            numeric_star = stars_mapping[word]
            return numeric_star  # Return the numeric value if found

# Test cases
print(sii('star-rating Three'))


        
