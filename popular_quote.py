import zmq
import json

QUOTES_FILE = "quotes.json"
RATINGS_FILE = "ratings.json"


def load_quotes():
    with open(QUOTES_FILE, "r") as file:
        return json.load(file)


def load_ratings():
    try:
        with open(RATINGS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_ratings(ratings):
    with open(RATINGS_FILE, "w") as file:
        json.dump(ratings, file, indent=4)


def rate_quote(quote, rating):
    ratings = load_ratings()
    if quote in ratings:
        ratings[quote].append(rating)
    else:
        ratings[quote] = [rating]
    save_ratings(ratings)


def get_average_rating(quote):
    ratings = load_ratings()
    if quote in ratings:
        return sum(ratings[quote]) / len(ratings[quote])
    return 0


def get_popular_quotes():
    quotes = load_quotes()
    ratings = load_ratings()
    popular_quotes = []

    for category, quote_list in quotes.items():
        for quote in quote_list:
            avg_rating = get_average_rating(quote)
            popular_quotes.append((quote, avg_rating))

    popular_quotes.sort(key=lambda x: x[1], reverse=True)
    return [quote[0] for quote in popular_quotes[:10]]


def popular_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    print("Popular Quote Microservice running on port 5558...")

    while True:
        message = socket.recv_string()

        if message.startswith("rate:"):
            parts = message.split("rate:", 1)[1].strip().split("|")
            quote = parts[0].strip()
            rating = int(parts[1].strip())
            rate_quote(quote, rating)
            response = f"Quote rated successfully: {quote} with {rating} stars."

        elif message == "view_popular":
            quotes = get_popular_quotes()
            response = "\n".join(quotes) if quotes else "No popular quotes available."

        socket.send_string(response)


if __name__ == "__main__":
    popular_main()