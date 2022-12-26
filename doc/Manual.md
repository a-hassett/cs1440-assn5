# Recursive Web Crawler User Manual

* In this program, you will provide a starter URL and possible a maximum depth of recursion. The program will then print every valid link that can be reached within that depth and the time it took to find them all.
* Before starting, make sure you have the `beautifulsoup4` and `requests` packages installed. If you don't, run these in your command line:
  * `$ pip install --user requests`
  * `$ pip install --user beautifulsoup4`
  * Make sure to put the --user part if you don't want them downloaded for every single user of your computer.
* When you run this program, you're gonna format the command line like this: `$ python src/crawler.py [STARTERURL] [optional: MAXDEPTH]`.
  * We will automatically assume that the first argument is the URL and the second is the maxDepth.
  * If there is no maxDepth given, we will assume it is 3.
* The starter URL must be an absolute URL that begins with either http or https
  * An absolute URL is one with a scheme like `http`, `https`, `ftp`, `telnet`, `ssh`, which is followed by the `://` token. Then a hostname follows that, which ends in domains like `.com`, `.org`, `.gov`, etc.
    * You can have stuff after the domain as well, but any fragments (beginning with "#") will be ignored.
    * A relative URL is one that doesn't have at least one of these requirements.
  * If a non-absolute URL or one starting with something other than "http" or "https" is given, you will get an error message telling you to provide an absolute URL
  * If no URL is given at all, you will get an error message asking you to provide one
* The max depth must be an integer that is greater than or equal to 0
  * If either of these two requirements is not met, the program will not run.
  * You will also get an error message for everything you did wrong.
* When all the links print, they will print with indentation based on when they were found, so you'll know where they came from.
* You can cancel the running of the program at any time by hitting `Ctrl+C` on your keyboard. You'll be let know that you hit those keys and that the program is exiting if you do.
* No matter if you quit early or wait for the program to complete, you will also be provided with the number of links you reached and how long it took.
