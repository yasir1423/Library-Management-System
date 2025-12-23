import json
import os

JSON_FILE = "library.json"

def load_data():
    # Show which file Python is using (helps if VSCode shows a different file)
    print("Using JSON file:", os.path.abspath(JSON_FILE))

    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Invalid JSON structure")
                # Ensure required keys exist
                data.setdefault("books", [])
                data.setdefault("borrowed_count", 0)
                return data
        except Exception:
            # If the file is empty or corrupted, reset to default structure
            return {"books": [], "borrowed_count": 0}
    # If file doesn't exist, return default structure
    return {"books": [], "borrowed_count": 0}

def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def add_book(data):
    title = input("Enter book title: ").strip()
    author = input("Enter the author's name: ").strip()
    # validate copies input
    while True:
        try:
            copies = int(input("Enter the number of copies: ").strip())
            if copies < 0:
                print("Please enter a non-negative integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for copies.")
    book = {"title": title, "author": author, "copies": copies}
    data["books"].append(book)
    save_data(data)
    print("Book added successfully!\n")

def borrow_book(data):
    title = input("Enter the book title to borrow: ").strip().lower()
    title = title.replace(":", "")  # fix accidental colon
    for book in data["books"]:
        # normalize both sides for reliable comparison
        if book.get("title", "").strip().lower() == title:
            if book.get("copies", 0) > 0:
                book["copies"] -= 1
                data["borrowed_count"] = data.get("borrowed_count", 0) + 1
                save_data(data)
                print("Book borrowed successfully!\n")
            else:
                print("Sorry! This book is not currently available.\n")
            return
    # executed only if loop completed with no match
    print("Book not found!\n")

def return_book(data):
    title = input("Enter the book title to return: ").strip().lower()
    title = title.replace(":", "")
    for book in data["books"]:
        if book.get("title", "").strip().lower() == title:
            book["copies"] = book.get("copies", 0) + 1
            # guard borrowed_count from going negative
            data["borrowed_count"] = max(0, data.get("borrowed_count", 0) - 1)
            save_data(data)
            print("Book returned successfully!\n")
            return
    print("Book not found in library records.\n")

def search_book(data):
    title = input("Enter the book title to search: ").strip().lower()
    title = title.replace(":", "")
    for book in data["books"]:
        if book.get("title", "").strip().lower() == title:
            print("\nBook found.")
            print("Title:", book.get("title"))
            print("Author:", book.get("author"))
            print("Available Copies:", book.get("copies", 0), "\n")
            return
    print("Book not found in library.\n")

def show_books(data):
    if not data.get("books"):
        print("No books in library!\n")
        return
    print("\n==== Library Books ====")
    for i, book in enumerate(data["books"], start=1):
        t = book.get("title", "Unknown")
        a = book.get("author", "Unknown")
        c = book.get("copies", 0)
        print(f"{i}. {t} by {a} (Copies: {c})")
    print("=======================\n")

def main():
    data = load_data()
    while True:
        print("=== LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Add book.")
        print("2. Borrow book.")
        print("3. Return book.")
        print("4. Search book.")
        print("5. Show all books.")
        print("6. Show total borrowed books.")
        print("7. Exit.")
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            add_book(data)
        elif choice == "2":
            borrow_book(data)
        elif choice == "3":
            return_book(data)
        elif choice == "4":
            search_book(data)
        elif choice == "5":
            show_books(data)
        elif choice == "6":
            print(f"Total borrowed books: {data.get('borrowed_count',0)}\n")
        elif choice == "7":
            print("Exiting the program... Good Bye")
            break
        else:
            print("Invalid Choice!!!\n")

if __name__== "__main__":
    main()