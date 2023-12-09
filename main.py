import requests
from bs4 import BeautifulSoup

# URL of the page
url = "https://ocimpact.com/delegate-roster/"
sub_url = "https://ocimpact.app.swapcard.com/widget/event/oc2023/people/RXZlbnRWaWV3XzQ1NTQwOA==?showActions=true"

# Send a GET request to the URL
response = requests.get(sub_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
        # find all the anchor tags with "href"  
    # attribute starting with "https://" 
    # for link in soup.find_all('div'): 
        # display the actual urls 
        #print(link.get('class'))

    # Find all delegates in the HTML
    delegates = soup.find_all('div', class_='wpb_wrapper')
    #  .find_all('div', class_='full_section_inner')

    # Create a list to store delegate information
    delegate_info_list = []
    #print("hello")
    print(delegates)
    # Iterate through each delegate
    for delegate in delegates:
        # Extract information for each delegate
        #print(delegate.find('div'))
        name = delegate.find('div', class_='name').text.strip()
        job_title = delegate.find('div', class_='title').text.strip()
        organization = delegate.find('div', class_='organization').text.strip()

        # Extract answers to questions
        questions = delegate.find_all('div', class_='question')
        answers = [question.find_next('div', class_='answer').text.strip() for question in questions]

        # Create a dictionary to store delegate information
        delegate_info = {
            'Name': name,
            'Job Title': job_title,
            'Organization': organization,
            'Answers': answers
        }

        # Append the delegate information to the list
        delegate_info_list.append(delegate_info)

    # # Print or process the delegate information
    # for delegate_info in delegate_info_list:
    #     print(delegate_info)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
