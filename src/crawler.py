import requests
from bs4 import BeautifulSoup  	         	  
from urllib.parse import urlparse, urljoin  	         	  
import sys  	         	  
import time  	         	  


def crawl(url, depth, maxDepth, visited):
    # remove fragment
    url = url.split("#")[0]

    # base cases
    if depth > maxDepth or url in visited:
        return

    # if the url gets to this point, it has required qualities
    visited.add(url)
    print("    " * depth, end="", file=sys.stderr)  # 4 spaces per depth
    print(url, file=sys.stderr)

    # check that the URL actually opens a webpage
    response = requests.get(url)
    if not response.ok:
        print(f"crawl({url}): {response.status_code} {response.reason}", file=sys.stderr)
        return

    # examine HTML file for new links
    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a')
    for a in links:
        link = a.get('href')
        if link:
            # create an absolute address from a (possibly) relative URL
            absoluteURL = urljoin(url, link)

            if absoluteURL.startswith('http'):
                crawl(absoluteURL, depth + 1, maxDepth, visited)
    return  	         	  


# If the crawler.py module is loaded as the main module, allow our `crawl` function to be used as a command line tool
if __name__ == "__main__":
    before = time.time()

    willExit = False
    if len(sys.argv) < 2:
        print("Error: no URL supplied", file=sys.stderr)
        exit(0)

    elif len(sys.argv) >= 2:
        startingUrl = sys.argv[1]
        maxDepth = 3  # this might get overridden later

        # check if startingUrl meets requirements
        if not bool(urlparse(startingUrl).netloc):  # if not absolute
            print("Error: Invalid URL supplied.", file=sys.stderr)
            print("Please supply an absolute URL to this program", file=sys.stderr)
            willExit = True
        elif not(startingUrl.startswith("https://") or startingUrl.startswith("http://")):
            print("URL must start with http or https", file=sys.stderr)
            willExit = True

    if len(sys.argv) > 2:
        # check if maxDepth meets requirements
        try:
            maxDepth = int(sys.argv[2])
            if maxDepth < 0:
                print("Depth must be greater than 0", file=sys.stderr)
                willExit = True
        except ValueError:
            print("Depth must be an integer", file=sys.stderr)
            willExit = True

    if willExit:
        exit(0)

    if maxDepth == 1:
        plural = ""
    else:
        plural = "s"

    print(f"Crawling from {startingUrl} to a maximum depth of {maxDepth} link{plural}", file=sys.stderr)

    visited = set()
    try:
        crawl(startingUrl, 0, maxDepth, visited)
    except KeyboardInterrupt:
        print("^ C", file=sys.stderr)
        print("Exiting...", file=sys.stderr)

    if len(visited) == 1:
        plural = ""
    else:
        plural = "s"

    after = time.time()

    print(f"Visited {len(visited)} unique page{plural} in {round(after - before, 4)} seconds", file=sys.stderr)
