from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Could not start the chat. Check initialization errors.")
        return
    
    pass

if __name__ == "__main__":
    main()