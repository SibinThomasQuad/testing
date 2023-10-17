import requests
import time

# Define the target URL
url = "https://google.com"  # Replace with the URL you want to test

# Define the number of requests to send
num_requests = 10  # Total number of requests to send
requests_per_second = 10  # Number of requests per second

# Initialize a list to store response times
response_times = []

# Send multiple requests at a specified rate
for _ in range(num_requests):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    # Calculate response time in milliseconds
    response_time_ms = (end_time - start_time) * 1000
    response_times.append(response_time_ms)

    # Optionally, check the response status code
    if response.status_code == 200:
        print(f"Request {len(response_times)}: Status Code 200, Response Time: {response_time_ms:.2f} ms")
    else:
        print(f"Request {len(response_times)}: Status Code {response.status_code}, Response Time: {response_time_ms:.2f} ms")

    # Control the request rate by sleeping
    time.sleep(1 / requests_per_second)

# Calculate and display statistics
avg_response_time = sum(response_times) / num_requests
min_response_time = min(response_times)
max_response_time = max(response_times)

print("\nLoad Test Results:")
print(f"Total Requests: {num_requests}")
print(f"Average Response Time: {avg_response_time:.2f} ms")
print(f"Minimum Response Time: {min_response_time:.2f} ms")
print(f"Maximum Response Time: {max_response_time:.2f} ms")
