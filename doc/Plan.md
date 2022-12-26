# Software Development Plan

## Phase 0: Requirements Specification *(10%)*

**Deliver:**

This program takes a given URL and looks at every website linked on that webpage.
We will print out each of those links, as long as they are actual webpages and haven't
been visited before. And we'll only go a few spaces deep.\
\
It starts with printing out "Crawling from [URL] to a maximum distance of [maxdepth]".
But this only happens after checking that the given URL is valid (meaning that it is
an absolute URL). If it's valid, we move onto the second given argument which should
be the maximum recursion depth. If there is none given, the default is three. I think
I'll also check that it's an integer greater than or equal to 0.\
\
After setting up the initial parts of the program, we have to web crawl. Each time we
do, we increase the current recursion depth by 1 as we get closer and closer to the
maxdepth we set at the beginning of the program. Also during each recursion, we get a 
URL to work with. We'll set up a set called `visited` at the beginning of the program
that will hold all the URL's we've seen before so that we don't use them again. So
when the recursion gives us an old URL, we just won't print it or look for anything
deeper. If the recursion gives us an absolute URL, we can use it directly for further
recursion. If it's not absolute, we can assume it's relative and use urljoin() to
get an absolute URL when combined with the link before. This means we'll have to check
for absolute-ness before putting it into the recursive method.\
\
We also need to keep track of the recursion depth, because we'll stop web crawling
at a certain depth, and the indentation of the URLs we print will be dependent on the 
depth as well (4 spaces per increase of 1 in depth). The base cases we'll need to check
at the beginning of the calling of the recursive functions are when currentdepth is greater
than maxdepth, when the URL is in the `visited` set already, or if the currentURL is not
valid. All of these conditions will stop that specific recursive branch.\
\
I'll need to figure out how to cancel the program when the user hits `Ctrl + C`. When
this happens, I will end the program and provide the runtime statistics (which are the
number of visited websites and the number of seconds it took). I'll be printing these 
statistics to sys.stderr as well. I think the `Ctrl + C` will be the hardest part for me.


## Phase 1: System Analysis *(10%)*

**Deliver:**

In the main method, I'll check for the number of sys.argv
arguments. If there is only 1, I'll print an error message that there was no URL given.
If there are two arguments but the website isn't properly formatted, I'll print an error
that an invalid URL was given and that it needs to be an absolute URL. If there are two
arguments but the URL is valid, I'll just continue on with maxdepth == 3. If there are three arguments
but the URL is invalid or the depth given isn't an integer, I'll print the errors for 
that and then exit the program. If they're both valid, I'll continue on. When I continue on I
will just be calling the recursive method which I will call `crawl`.\
\
My main recursive function `crawl` will take url, depth, maxdepth, and visited as parameters. 
I'll start by checking for base cases which will return nothing if they succeed. If they don't succeed
I'll perform my web crawl as normal.
The url parameter will be used to open a webpage and find new links using the `<a>` attribute. I can use the
same technique used in `findLinks` in the demo for BeautifulSoup. I think I'll make a method for 
this too because it's also a bit messy. I'll use the links it gives me and put them in a list.
Then for every item in the list, I'll check if it's an absolute URL and possibly use urljoin. If 
I end up using urljoin I will change the item in the list I was just talking about to match the
new absolute URL. I'll print the link with enough spaces for 4 times the currentdepth count.
If it's not a valid URL, I'll use try/except to print an error message without crashing the
program. Then I'll call `crawl` recursively for each of the items in the list.
I'll need to add each URL I try to the visited set.\
\
I'll need a statistics method with parameters (before, after, urls) where I can print
the runtime in seconds and the number of visited websites, which will be the length of the
`visited` set. I'll make it a method because we either call it at the end or whenever we
get a `Ctrl + C` from the user. I'll have a method that will check if a URL is absolute or
not because we do that in multiple places, and it'll be cleaner to do it outside the main
functionalities anyway. The HTML file
we will print the output to will be named with "level[maxdepthcount].html".\
\
After all of the recursions are done, I'll print out the statistics using my statistics
method. I think I'll also put the check for `Ctrl + C` at the beginning of each recursive 
call to `crawl`. 


## Phase 2: Design *(30%)*

**Deliver:**

```python
def crawl(url, depth, maxdepth, visited):
    # i might have to put this entire this in a try block and put except
    # at the bottom where I'll check for KeyboardInterrupt
    url = remove fragment
    if depth > maxdepth or url in visited or not urlisvalid:
        return
    elif Ctrl + C:
        after = gettime()
        printStatistics(before, after, len(visited))
        exit(0)        
    links = find links
    if links:
        for i in range(len(links)):
            visited.add(links[i])
            if urlisvalid(links[i]):
                links.append(urljoin(url, links[i]))
                print("    " * depth, end="")  # 4 spaces per depth
                print(url)
                crawl(links[i], depth + 1, maxdepth, visited)
```
```python
def printStatistics(before, after, numLinks):
    print(f"Visited {numLinks} unique pages in {after - before} seconds", file=sys.stderr)
```
```python
def isValid(url):
    # this function will just be checking whether the url is absolute
    # i might want to change the name to isAbsolute(url)
    response = get(url)
    if response:
        return True
    else:
        return False
```
```python
def main():
    if len(sys.argv) == 1:
        print("Error: no URL supplied")
        exit(0)
    elif len(sys.argv) == 2:
        if(urlisvalid(sys.argv[1])):
            url = sys.argv[1]
            maxdepth = 3
        else:
            print("Error: Invalid URL supplied.")
            print("Please supply an absolute URL to this program")
            exit(0)
    elif len(sys.argv) == 3:
        willExit = False
        if(urlisvalid(sys.argv[1])):
            url = sys.argv[1]
        else:
            print("Error: Invalid URL supplied.")
            print("Please supply an absolute URL to this program")
            willExit = True
        if(sys.argv[2] > 0):
            try:
                maxdepth = int(sys.argv[2])
            except ValueError:
                print("Depth must be an integer")
                willExit = True
        else:
            print("Depth must be greater than 0")
        if willExit:
            exit(0)
    
    visited = set()
    crawl(url, 0, maxdepth, visited)
```


## Phase 3: Implementation *(15%)*

**Deliver:**

A lot of my pseudocode was quite a bit off from what it was supposed to be. I didn't use
the existing code when writing my pseudocode, so I had to copy and paste some lines, and many
didn't transfer over at all. I decided against making an isAbsolute() method and printStatistics()
method because each of them only contained one line of code and was only used in one place. This
isn't how I thought it would work, but it's alright. Usually my pseudocode is better, but I had 
to rework pretty much all of it to fit the existing structure of `crawler.py`. It's okay,
though. The best part about my pseudocode was that it contained all of the stuff I am supposed
to keep track of. Even though it wasn't in the right spots, it was in there somewhere so I 
didn't forget most things. I switched up my main method, too. Instead of checking the requirements
for 3 different lengths of sys.argv, I assumed that the length could be anywhere from 0 to
infinity. Then I checked that the URL was good. If sys.argv is long enough, I checked
that maxDepth was good (integer greater than or equal to 0). 


## Phase 4: Testing & Debugging *(30%)*

**Deliver:**

I looked at the Output.md file and made sure my program matched its output exactly.
When I started looking at more possible cases, I realized that the links I was printing
were slightly off. It was printing links that were an attempt to visit, instead of ones that
actually ended up working. Like the starting URL wouldn't get printed, and the links that fulfilled
the base cases were printed, but they weren't supposed to be. I ended up finding that it happened
because I automatically printed the URL's as I was finding them instead of in a place in the code that
would ensure the URLs at that location were perfect. I also realized when looking at the example 
output that the seconds in the
runtime count was supposed to be rounded to 4 spaces, so I fixed that. I double checked that all my 
print statements printed to sys.stderr. Then I checked for any remaining to-do statements and
reformatted some code to look prettier. I also added a few comments. None of these things were really
bugs though. The biggest bug was that the wrong links were being printed.


## Phase 5: Deployment *(5%)*

**Deliver:**

*   Your repository pushed to GitLab.
*   **Verify** that your final commit was received by browsing to its project page on GitLab.
    *   Ensure the project's URL is correct.
    *   Review the project to ensure that all required files are present and in correct locations.
    *   Check that unwanted files have not been included.
    *   Make any final touches to documentation, including the Sprint Signature and this Plan.
*   **Validate** that your submission is complete and correct by cloning it to a new location on your computer and re-running it.
	*	Run your program from the command line so you can see how it will behave when your grader runs it.  **Running it in PyCharm is not good enough!**
    *   Run through your test cases to avoid nasty surprises.
    *   Check that your documentation files are all present.


## Phase 6: Maintenance

**Deliver:**

* If you don't take it slow, in the main method, my original search for errors in the given command line arguments is a little choppy. I wrote it to avoid repetition, but it's a bit hard to look at. Also, I think there's a better way to remove the fragment from the URL, but I couldn't find anything better in the demos or online.
* I don't understand very much of the pre-written code, like the parts with BeautifulSoup and requests.
* It might take me a little while, but I don't think it would be too bad. I added comments for most of the sections of code so I can skim through pretty easily. However, a lot of my code is based on the exact order of the lines, and I'd probably have some trouble not making new bugs when fixing the old one.
* My documentation is pretty well-thought-out, because I took notes separately as I read through the instructions before starting Phase 0 and 1.
* It might take a minute for someone else to read through, but I think that's pretty normal.
* It might be a little difficult to add features to this program in a year, because it is written in two functions, and the variables are spread out a bit haphazardly.
* A change in computer hardware shouldn't change my program. It might make it run a little faster.
* A change in the OS probably won't change its function either.
* The next version of Python could have some changes, but hopefully not too significant. I say this because as I was doing this assignment I came across an article talking about the differences between Beautiful Soup for Python 2 and Python 3.
