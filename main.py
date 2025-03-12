import zmq


def main():
    # Set up ZeroMQ context and sockets for all microservices
    context = zmq.Context()

    # Socket for favorite quotes (existing microservice)
    fav_socket = context.socket(zmq.REQ)
    fav_socket.connect("tcp://localhost:5555")  # Port for fav_quote.py

    # Socket for filtering quotes by category (Microservice B)
    filter_socket = context.socket(zmq.REQ)
    filter_socket.connect("tcp://localhost:5556")  # Port for filter_quote.py

    # Socket for searching quotes by keyword (Microservice C)
    search_socket = context.socket(zmq.REQ)
    search_socket.connect("tcp://localhost:5557")  # Port for search_quote.py

    # Socket for popular quotes and rating (Microservice D)
    popular_socket = context.socket(zmq.REQ)
    popular_socket.connect("tcp://localhost:5558")  # Port for popular_quote.py

    print("All microservices connected. Ready to interact!")

    while True:
        print("\n--------------------------------------------------------------------")
        print("\nWhat would you like to do?")
        print("1. Save a quote to favorites")
        print("2. View favorite quotes")
        print("3. Remove a quote from favorites")
        print("4. Filter quotes by category")
        print("5. Search quotes by keyword")
        print("6. View popular quotes")
        print("7. Rate a quote")
        print("8. Exit")

        user_input = input("Enter your choice: ")

        # Save a quote to favorites
        if user_input == "1":
            quote = input("Enter the quote you want to save: ").strip()
            print(f"Sending request to save quote: {quote}")
            fav_socket.send_string(f"save:{quote}")
            response = fav_socket.recv_string()
            print(response)

        # View favorite quotes
        elif user_input == "2":
            print("Sending request to view favorite quotes...")
            fav_socket.send_string("view_fav")
            response = fav_socket.recv_string()
            print("\nYour favorite quotes:\n")
            print(response)

        # Remove a quote from favorites
        elif user_input == "3":
            print("Sending request to view favorite quotes...")
            fav_socket.send_string("view_fav")
            response = fav_socket.recv_string()

            if response == "No favorite quotes saved.":
                print(response)
                continue

            print("\nYour favorite quotes:\n")
            print(response)

            quote_number = input("\nEnter the number of the quote you want to remove: ")

            if not quote_number.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            print(f"Sending request to remove quote number {quote_number}...")
            fav_socket.send_string(f"remove:{quote_number}")
            response = fav_socket.recv_string()
            print(response)

        # Filter quotes by category
        elif user_input == "4":
            print("\nAvailable categories: motivation, success, life")
            category = input("Enter the category you want to filter by: ").strip()
            print(f"Sending request to filter quotes by category: {category}")
            filter_socket.send_string(f"filter:{category}")
            response = filter_socket.recv_string()
            print(f"\nQuotes in category '{category}':\n")
            print(response)

        # Search quotes by keyword
        elif user_input == "5":
            keyword = input("Enter the keyword you want to search for: ").strip()
            print(f"Sending request to search quotes by keyword: {keyword}")
            search_socket.send_string(f"search:{keyword}")
            response = search_socket.recv_string()
            print(f"\nSearch results for '{keyword}':\n")
            print(response)

        # View popular quotes
        elif user_input == "6":
            print("Sending request to view popular quotes...")
            popular_socket.send_string("view_popular")
            response = popular_socket.recv_string()
            print("\nPopular quotes:\n")
            print(response)

        # Rate a quote
        elif user_input == "7":
            quote = input("Enter the quote you want to rate: ").strip()
            rating = input("Enter your rating (1-5): ").strip()

            if not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                print("Invalid rating. Please enter a number between 1 and 5.")
                continue

            print(f"Sending request to rate quote: {quote} with {rating} stars...")
            popular_socket.send_string(f"rate:{quote}|{rating}")
            response = popular_socket.recv_string()
            print(response)

        # Exit the program
        elif user_input == "8":
            print("Exiting the program. Goodbye!")
            break

        # Invalid input
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
