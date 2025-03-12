import zmq
import json

QUOTES_FILE = "quotes.json"


def load_quotes():
    with open(QUOTES_FILE, "r") as file:
        return json.load(file)


def search_quotes_by_keyword(keyword):
    quotes = load_quotes()
    results = []
    for category, quote_list in quotes.items():
        for quote in quote_list:
            if keyword.lower() in quote.lower():
                results.append(quote)
    return results


def search_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    print("Search Quote Microservice running on port 5557...")

    while True:
        message = socket.recv_string()

        if message.startswith("search:"):
            keyword = message.split("search:", 1)[1].strip()
            quotes = search_quotes_by_keyword(keyword)
            response = "\n".join(quotes) if quotes else "No quotes found with this keyword."

        socket.send_string(response)


if __name__ == "__main__":
    search_main()