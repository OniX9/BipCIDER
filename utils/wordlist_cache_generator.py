def wordlist_cache_generator():
    print("Reading words from wordlist/english.txt...")

    with open("wordlist/english.txt", "r") as file:
        formatted_words = file.read().split()  # Read and split words from the file

    print("Caching words_list...")

    with open("wordlist/wordslist_cache.py", "w") as file:
        file.write(f"bip32_words = {formatted_words}\n")

    print("Words have been formatted and saved in wordslist_cache.txt")


# wordlist_cache_generator()