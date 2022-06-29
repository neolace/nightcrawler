
# NightCrawler v1.6

## NightCrawler Web Scraper

NightCrawler is a tool developed in Python that we can use as a foot-printing tool against our own web pages.

NightCrawler is Object-Oriented (a Class), so you can reuse the code for make a better (more interesting?) program. 
The code at this point only follows links to web pages, not to binary files, but you can reuse the data that the "crawler" object generates.

**To manually create a virtualenv on Linux:**

```
$ python -m venv .env
```

**step to activate your virtualenv.**

```
$ source .env/bin/activate
```

**If you are a Windows platform, you would activate the virtualenv like this:**

```
% .env\Scripts\activate.bat
```

**Once the virtualenv is activated, you can install the required dependencies.**

```
$ pip install -r requirements.txt
```

**Change the root value**

```
root = "http://www.google.com/"
```

Now just run the script: nightcrawler.py
