import zmq


def test_filter_quotes():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")  # Connect to Microservice B

    # Send a request to filter quotes by category
    category = "motivation"  # Change this to test other categories
    socket.send_string(f"filter:{category}")
    response = socket.recv_string()
    print(f"Filtered Quotes (Category: {category}):\n{response}\n")


def test_search_quotes():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")  # Connect to Microservice C

    # Send a request to search quotes by keyword
    keyword = "success"  # Change this to test other keywords
    socket.send_string(f"search:{keyword}")
    response = socket.recv_string()
    print(f"Search Results (Keyword: {keyword}):\n{response}\n")


def test_popular_quotes():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")  # Connect to Microservice D

    # Send a request to view popular quotes
    socket.send_string("view_popular")
    response = socket.recv_string()
    print(f"Popular Quotes:\n{response}\n")


def test_rate_quote():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5558")  # Connect to Microservice D

    # Send a request to rate a quote
    quote = "Believe you can and you're halfway there."
    rating = 5  # Change this to test other ratings
    socket.send_string(f"rate:{quote}|{rating}")
    response = socket.recv_string()
    print(f"Rating Response:\n{response}\n")


if __name__ == "__main__":
    test_filter_quotes()
    test_search_quotes()
    test_popular_quotes()
    test_rate_quote()
