import zmq
import json

FAVORITES_FILE = "favorites.json"

#loading the favorite json file
def load_quotes():
    with open(FAVORITES_FILE, "r") as file:
        return json.load(file)
    
def save_quote(quote):
    with open(FAVORITES_FILE, "w") as file:
        json.dump(quote, file, indent=4)

def add_to_favorites(quote):
    favorites = load_quotes() #loading existing quotes

    if quote in favorites:
        return "Quote is already in favorites."
    
    favorites.append(quote)
    save_quote(favorites)

    return f"Quote successfully saved!"

def show_fav_quote():
    favorites = load_quotes()

    if not favorites:
        return "No favorite quotes saved."

    return "\n".join([f"{i+1}. {quote}" for i, quote in enumerate(favorites)])

def get_quote(index):
    favorites = load_quotes()  # Load the quotes without modifying them

    if index < 1 or index > len(favorites):
        return "Invalid quote number.", None  # Return None when the index is invalid

    return favorites[index - 1], favorites[index - 1]  # Return the quote itself

def remove_quote(index):
    favorites = load_quotes()

    if index < 1 or index > len(favorites):
        return "Invalid quote number.", None  #return None when the index is invalid

    removed_quote = favorites.pop(index - 1)
    save_quote(favorites)

    return f"Successfully removed: {removed_quote}", removed_quote  #return both message and the removed quote


def fav_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Manage Favorite Quote System running on port 5555...")

    while True:
        message = socket.recv_string()

        if message.startswith("save:"):
            quote = message.split("save:", 1)[1].strip()  #extract the quote
            response = add_to_favorites(quote)
            print(f"Received request {message}, now saving the quote...")

        elif message == "view_fav":
            response = show_fav_quote()
            print(f"Received request '{message}', now fetching a list of favorite quotes...")

        elif message.startswith("get:"): #get the quote number but not remove yet
            index = int(message.split("get:", 1)[1].strip())
            response, quote = get_quote(index) 
            if quote is None:
                response = "Invalid quote number."
            else:
                response = quote  #send the quote itself as response

        elif message.startswith("remove:"):
            index = int(message.split("remove:", 1)[1].strip())
            response, _ = remove_quote(index)  #get both response message and removed quote
            print(f"Received request '{message}', now removing quote number {index}...")

        socket.send_string(response)

fav_main()