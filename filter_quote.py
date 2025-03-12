import zmq
import json

QUOTES_FILE = "quotes.json"


def load_quotes():
    with open(QUOTES_FILE, "r") as file:
        return json.load(file)


def filter_quotes_by_category(category):
    quotes = load_quotes()
    return quotes.get(category, [])


def filter_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Filter Quote Microservice running on port 5556...")

    while True:
        message = socket.recv_string()

        if message.startswith("filter:"):
            category = message.split("filter:", 1)[1].strip()
            quotes = filter_quotes_by_category(category)
            response = "\n".join(quotes) if quotes else "No quotes found in this category."

        socket.send_string(response)


if __name__ == "__main__":
    filter_main()