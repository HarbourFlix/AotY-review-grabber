import requests
from bs4 import BeautifulSoup
import time

# returns a list of all links by the user
def getReviewLinks(base_url, headers):
	# some reviews are short enough to be displayed on the "user/-/reviews"-page, but that's only for really short ones
	# thus we collect the links and grab the reviews' text later 
	links = []

	# getting the maximum amount of pages of reviews from the page selector at the bottom of the "reviews" page
	response = requests.get(base_url, headers=headers)  
	soup = BeautifulSoup(response.content, 'html.parser')  

	pages = soup.findAll("div", class_="pageSelectSmall")
	maxPage = 1 + int(pages[len(pages)-1].get_text(separator='\n').strip()) # take the text out of the last "pageSelectSmall" div

	for page in range(1, maxPage):
		url = f"{base_url}{page}/"  # URL for the current page
		response = requests.get(url, headers=headers)  # get the current page

		
		# breaks the loop, if the request isn't successful
		if response.status_code != 200:
			print("status error")
			break

		soup = BeautifulSoup(response.content, 'html.parser') # parse the HTML
		
		# takes all elements of class "gray", which contain the links to the reviews
		allReviewLinks = soup.findAll('a', class_="gray")
		for nextLink in allReviewLinks:
			# "href" gives the link, we .get it and append it to the list
			links.append(f"https://www.albumoftheyear.org{nextLink.get('href')}")

		print(f"currently on page {page}/11") # counter

		time.sleep(1)  # sleep to avoid complications with the server
	return links		

def getReviewsFrom(headers, links):
	reviews = []

	# iterates through the links 
	for url in links:
		response = requests.get(url, headers=headers)

		# breaks the loop, if the request isn't successful
		if response.status_code != 200:
			print("status error")
			break

		soup = BeautifulSoup(response.content, 'html.parser')  # parse the HTML

		# grabs the review div and extracts the text & appends it to the list
		reviewDiv = soup.find('div', class_="userReviewText")
		review = reviewDiv.get_text(separator='\n').strip()

		reviews.append(f"\n{url}:\n{review}")

		print(f"review {links.index(url)+1}/{len(links)}") # counter

		time.sleep(0.3) # sleep to avoid complications with the server

	return reviews


def grabReviews(user, header):
	base_url = f"https://www.albumoftheyear.org/user/{user}/reviews/"
	reviews = []  # stores the reviews 
	headers = {'User-Agent': header} # aoty throws 403 for get-requests without a header 

  # get links for all reviews
	links = getReviewLinks(base_url, headers)

  # get the reviews themselves
	reviews = getReviewsFrom(headers, links)

	return reviews  


if __name__ == "__main__":
	user = "/"  # placholder for username 
  header = "/" # placeholder for header
	reviews = grabReviews(user, header)
