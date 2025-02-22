import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555") #using port 5555

    #example program
    while True:
        print("\n--------------------------------------------------------------------")
        print("\nWhat would you like to do?")
        print("1. save quote")
        print("2. get user's favorite quotes ")
        print("3. remove quote from favorites")
        print("4. exit")

        user_input = input("Enter your choice: ")

        if user_input == "1":
            #this is a random quote which I hard coded in. You should replace this quote with the quotes from your display quote function
            quote = "this is a random quote for testing"
            print(quote)

            save_option = input("Do you want to save this quote? (Yes/No): ").strip().lower()
            if save_option == "yes":
                socket.send_string(f"save:{quote}")  #send remove request with type
                response = socket.recv_string() #should respond with saved successfully
                print(response)
            elif save_option == "no":
                print("Quote not saved.")
            else:
                print("Invalid input. Returning to the main menu.")
    
        #get a list of favorite quotes
        elif user_input == "2":
            socket.send_string("view_fav")
            print("\nHere is a list of your favorite quotes: \n")
            response = socket.recv_string() #should respond with a list of quotes
            print(response) 

        elif user_input == "3":
            socket.send_string("view_fav") #we get a list of user's favorite quotes
            response = socket.recv_string()
            
            #if no fav quotes
            if response == "No favorite quotes saved.":
                print(response)
                continue

            print("\nHere is a list of your favorite quotes: \n")
            print(response)

            quote_number = input("\nEnter the number of the specific quote that you wish to remove from favorites: ")

            #error handling
            if not quote_number.isdigit():
                print("Invalid input, try again.")
                quote_number = input("\nEnter the number of the specific quote that you wish to remove from favorites: ")

            #we send the quote number which user entered
            socket.send_string(f"get:{quote_number}")
            quote_to_remove = socket.recv_string() #receives the quote number as response

            #if the number is out of bound
            if quote_to_remove == "Invalid quote number.":
                print(quote_to_remove)
                continue

            #asking user to double confirm
            confirm = input(f"Are you sure you want to remove QUOTE {quote_number} from favorites? (Yes/No): ").strip().lower()
            if confirm == "yes":
                socket.send_string(f"remove:{quote_number}")
                response = socket.recv_string()
                print(response)
            else:
                print("Operation canceled.")


        elif user_input == "4":
            return
        
main()