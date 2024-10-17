import requests
from bs4 import BeautifulSoup

def get_all_nested_tags(soup):
    tags_with_attributes = {}
    
    for tag in soup.find_all(True):  # Find all tags
        tag_name = tag.name
        attributes = tag.attrs
        
        # If the tag is not already in the dictionary, add it
        if tag_name not in tags_with_attributes:
            tags_with_attributes[tag_name] = []
        
        # Append attributes to the tag's list
        tags_with_attributes[tag_name].append(attributes)
    
    return tags_with_attributes

def print_nested_tags(soup, level=0):
    # Print the current level of tags
    for tag in soup.find_all(True):
        print("  " * level + f"<{tag.name}>")
        # Recursively print nested tags
        print_nested_tags(tag, level + 1)

def scrape_tags(url):
    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Print all nested tags
        print("Nested HTML Tags:")
        print_nested_tags(soup)
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")

if __name__ == '__main__':
    url = input("Enter the URL of the website: ")
    scrape_tags(url)
