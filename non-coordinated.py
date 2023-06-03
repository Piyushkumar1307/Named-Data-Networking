import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_program():
    # Get user input for Zipf's distribution parameter "a"
    a = float(input("Enter the value for Zipf's distribution parameter 'a': "))

    # Generate content names using Zipf distribution
    content_names = np.random.zipf(a=a, size=200)

    # Convert content names to strings
    content_names = content_names.astype(str)

    # Calculate the popularity counts
    popularity_counts = pd.Series(content_names).value_counts().reset_index()
    popularity_counts.columns = ['Content Name', 'Popularity Count']

    # Add a random timestamp for content names with the same popularity
    timestamps = pd.to_timedelta(np.random.randint(0, 1000, size=len(popularity_counts)), unit='m')
    popularity_counts['Timestamp'] = pd.Timestamp('now') - timestamps

    # Sort the table by popularity count in descending order
    popularity_counts = popularity_counts.sort_values(by='Popularity Count', ascending=False)

    # Reset the index
    popularity_counts = popularity_counts.reset_index(drop=True)

    # Calculate skewness for each content name
    skewness = popularity_counts['Popularity Count'].skew()

    # Create a router with cache count 3
    class Router:
        def __init__(self, cache_count):
            self.cache_count = cache_count
            self.cache = []
            self.hit_count = 0
            self.access_count = 0

        def update_cache(self, content_name, popularity_count):
            # Check if the cache has reached the specified count
            if len(self.cache) >= self.cache_count:
                # Find the least popular content in the cache
                least_popular_content = min(self.cache, key=lambda x: x['Popularity Count'])

                # Remove the least popular content from the cache
                self.cache.remove(least_popular_content)

            # Add the new content to the cache
            self.cache.append({'Content Name': content_name, 'Popularity Count': popularity_count})

        def print_cache_contents(self):
            print("Router's Cache Contents:")
            for content in self.cache:
                print(f"Content Name: {content['Content Name']}, Popularity Count: {content['Popularity Count']}")

        def access_cache(self, content_name):
            self.access_count += 1
            for content in self.cache:
                if content['Content Name'] == content_name:
                    self.hit_count += 1
                    return True
            return False

        def get_hit_ratio(self):
            if self.access_count == 0:
                return 0.0
            return (self.hit_count / self.access_count) * 100

    # Create a router instance with cache count 3
    router = Router(cache_count=3)

    # Get the top 3 popular content names
    top_content_names = popularity_counts['Content Name'][:3]
    top_content_popularity = popularity_counts['Popularity Count'][:3]

    # Store the top content names in the router's cache
    for content_name, popularity_count in zip(top_content_names, top_content_popularity):
        router.update_cache(content_name, popularity_count)

    # Print the generated content names (Zipf distribution)
    print("Generated Content Names (Zipf distribution):")
    print(content_names)

    # Generate permutations of the content names
    permutations = np.random.permutation(content_names)

    # Print the generated content names (permutations)
    print("Generated Content Names (Permutations):")
    print(permutations)

    # Print the popularity count table
    print("Popularity Count Table:")
    print(popularity_counts)

    # Print the router's cache contents before user input
    router.print_cache_contents()

    # User input a content name to add to the router's cache
    user_input = input("Enter a content name to add to the router's cache: ")
    least_popularity_count = min(popularity_counts['Popularity Count'])
    router.update_cache(user_input, least_popularity_count)

    # Print the router's cache contents after user input
    router.print_cache_contents()

    # Calculate the hit ratio for each unique content in permutations
    hit_ratios = []
    for content_name in np.unique(permutations):
        is_hit = router.access_cache(content_name)
        hit_ratio = router.get_hit_ratio()
        hit_ratios.append(hit_ratio)
        print(f"Content: {content_name}, Hit Ratio: {hit_ratio:.2f}%")

    # Calculate the average hit ratio
    average_hit_ratio = np.mean(hit_ratios)
    print(f"\nHit Ratio of router: {average_hit_ratio:.2f}%")

    # Plot the content graph
    plt.figure(figsize=(10, 6))
    plt.bar(popularity_counts['Content Name'], popularity_counts['Popularity Count'])
    plt.xlabel('Content Name')
    plt.ylabel('Popularity Count')
    plt.title('Content Graph (Skewness: {:.2f}, zipfs parameter(a): {:.2f})'.format(skewness, a))
    plt.xticks(rotation=90)
    plt.show()

    # Plot the hit ratio graph
    plt.figure(figsize=(10, 6))
    plt.plot(np.unique(permutations), hit_ratios, marker='o', linestyle='-', color='b')
    plt.xlabel('Content Name')
    plt.ylabel('Hit Ratio (%)')
    plt.title('Hit Ratio (a: {:.2f})'.format(a))
    plt.xticks(rotation=90)
    plt.show()

# Loop to ask the user if they want to rerun the program
while True:
    run_program()
    choice = input("Do you want to rerun the program? (yes/no): ")
    if choice.lower() != 'yes':
        break
