import time
from html.parser import HTMLParser
from urllib.parse import urlsplit
import requests

# Change this value for the web page domain that you want to crawl
# Don't forget the "http://" part
root = 'https://www.example.com/'
# Time out time for http connections
timeout: tuple[int, int] = (5, 10)

version = 1.6


class Parse(HTMLParser):
    """
        Parse HTML text
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.href = []
        self.ctag = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.ctag = tag
            for at in attrs:
                if at[0] == 'href':
                    my_href = at[1].encode('ascii', 'ignore').strip()
                    if my_href:
                        self.href.append(my_href)
        else:
            self.ctag = ''

    def handle_endtag(self, tag):
        # print "Encountered an end tag :", tag
        pass

    def handle_data(self, data):
        if self.ctag == 'a':
            self.data.append(data)

    @property
    def get_data(self):
        return self.data[:]

    @property
    def get_href(self):
        return self.href[:]

    def clear(self):
        self.data = []
        self.href = []
        self.ctag = ''


def parse_base_url(url):
    """
        Create a valid base url

        @param url: Url to clean
        @type url: string
    """
    r1 = urlsplit(url)
    r1 = ('{0}://{1}/', r1.scheme, r1.netloc)
    return r1


def clean_url(url):
    """
        Clear url parameters and query

        @param url: Url to clean
        @type url: string
    """
    r1 = urlsplit(url)
    r1 = ('{0}://{1}{2}', r1.scheme, r1.netloc, r1.path)
    return r1


def get_contype(headerct=''):
    """
        Return MIME type from a valid 'content-type' HTTP header

        @param headerct: content-type
        @type headerct: string
    """

    content_type = headerct.split(';')
    content_type = content_type[0].strip()
    return content_type


class Crawler(object):
    """
        Main crawler object
    """

    def __init__(self, roote):
        self.base_url = parse_base_url(roote)
        # This is a list because we want
        # all our elements in an ordered sequence,
        # so we can traverse the list by an index
        self.child_links = [self.base_url]
        # This variables can be "sets" because
        # we don't want duplicate elements
        self.broken_links = set()
        self.email_accounts = set()
        self.tel_nums = set()
        self.name = set()
        self.surname = set()
        self.title = set()
        self.company = set()
        self.job = set()
        self.department = set()
        self.office = set()
        self.fax = set()
        self.phone_numbers = set()
        self.mobile = set()
        self.website = set()
        self.address = set()
        self.city = set()
        self.state = set()
        self.zip = set()
        self.country = set()
        self.country_code = set()
        self.currency = set()
        self.timezone = set()
        self.crawl_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.version = version
        self.lang = set()
        self.parse = Parse()
        self.map_files(roote)

    def map_files(self, url):
        """
            This function first verifies if the url has the valid MIME type
            and then calls fetch_links_from_url() to parse the HTML data

            @param url: Base url from where to start crawling
            @type url: string
        """

        rq = None
        mfiles = []
        r1 = urlsplit(url)
        if not r1.scheme and not r1.netloc:
            url = self.base_url

        print('\n+ Crawling: {0}', url)

        rq = requests.get(url, timeout=timeout)

        # Don't proceed if this page don't exist
        if rq.status_code != 200:
            rq.raise_for_status()

        # Check for content-type == text/html
        contype = get_contype(rq.headers['content-type'])
        print('    - Content-Type:', contype)

        if contype != 'text/html':
            print('\tERROR: Is not a text/html\n')
            return mfiles

        # Parse page and search links
        self.fetch_links_from_url(rq.text, url)

    def start(self):
        """
            Trigger function that starts to fetch links from self.base_url
        """

        time_start = time.time()
        print('NightCrawler v{0}', version)
        print('Please stand by ...\n')
        print('BASE URL: {0}', self.base_url)

        # This variable is my index for the list of child links
        # we are going to analyze child by child until there
        # are no more new children
        i = 0

        while i < len(self.child_links):
            self.map_files(str(self.child_links[i]))
            i += 1

        print()
        print('-' * 32)
        print('Results:')
        print('{0:d} email accounts, {1:d} tel. numbers and {2:d} links' 
              '({3:6f} seconds) ... \n', len(self.email_accounts), len(self.tel_nums), len(self.child_links),
              str(time.time() - time_start))
        print('Links:')
        print(self.child_links)
        print('Emails:')
        print(self.email_accounts)
        print('Tel:')
        print(self.tel_nums)
        print('Phone:')
        print(self.phone_numbers)

    def fetch_links_from_url(self, base_text='', url=''):
        """
        Parse a webpage and return a list of valid links (urls)

        @param base_text: HTML Content
        @type base_text: string
        @param url: Url
        """

        prep_url = clean_url(url)

        print('+ Fetch children from Base url:', prep_url)

        # Parse the HTML code
        parser = Parse()
        parser.feed(base_text)

        # It's possible to use the other data parsed
        # e.g. Search in the data for emails, phones, etc
        # data = parser.getdata()

        # Get links that the parser fetched from the "a" tags
        url_list = parser.get_href
        print("URLS FOUND: {0}", url_list)
        print("PREP URL: {0}}", prep_url)

        # Iterate over the urls and get all the possible children
        for u in url_list:
            tmp_url_src = urlsplit(u)

            tmp_path = tmp_url_src.path.decode('utf-8').strip()
            tmp_scheme = tmp_url_src.scheme.decode('utf-8')
            tmp_netloc = tmp_url_src.netloc.decode('utf-8')

            # Skip email addresses
            if tmp_scheme == 'mailto':
                self.email_accounts.add(tmp_path)
                continue
            if tmp_scheme == 'tel':
                self.tel_nums.add(tmp_path)
                continue
            if tmp_scheme == "name":
                self.name.add(tmp_path)
                continue
            if tmp_scheme == "surname":
                self.surname.add(tmp_path)
                continue
            if tmp_scheme == "address":
                self.address.add(tmp_path)
                continue
            if tmp_scheme == "city":
                self.city.add(tmp_path)
                continue
            if tmp_scheme == "state":
                self.state.add(tmp_path)
                continue
            if tmp_scheme == "country":
                self.country.add(tmp_path)
                continue
            if tmp_scheme == "zip":
                self.zip.add(tmp_path)
                continue
            if tmp_scheme == "title":
                self.title.add(tmp_path)
                continue
            if tmp_scheme == "company":
                self.company.add(tmp_path)
                continue
            if tmp_scheme == "job":
                self.job.add(tmp_path)
                continue
            if tmp_scheme == "department":
                self.department.add(tmp_path)
                continue
            if tmp_scheme == "office":
                self.office.add(tmp_path)
                continue
            if tmp_scheme == "fax":
                self.fax.add(tmp_path)
                continue
            if tmp_scheme == "phone":
                self.phone_numbers.add(tmp_path)
                continue
            if tmp_scheme == "mobile":
                self.mobile.add(tmp_path)
                continue
            if tmp_scheme == "website":
                self.website.add(tmp_path)
                continue

            # Skip urls not in my domain
            if tmp_netloc not in self.base_url:
                continue

            # Black List
            # Skip binary files (we only want web pages for now)
            black_list = False
            for ext_path in [".jpg", ".jpeg", ".pdf", ".doc", ".docx", ".xlsx", ".jfif", ".xl", ".png", ".gif", ".mp",
                             ".exe", ".zip", ".rar", ".7z", ".tar", ".gz", ".jar"]:
                if ext_path in tmp_path:
                    black_list = True

            if black_list:
                continue

            # Skip empty links and relative urls
            if not tmp_path or tmp_path == '/':
                continue

            # Remove trailing /
            if tmp_path[0] == '/':
                tmp_path = tmp_path[1:]

            # Continue to the next if already on children list
            # Skip urls in broken links
            if tmp_path in self.child_links or tmp_path in self.broken_links:
                continue

            try:
                rq = requests.get(tmp_path, timeout=timeout)
            except Exception as er:
                print('Connection error (3) > {0}{1}', tmp_path, er)
                self.broken_links.add(tmp_path)
                continue

            # Don't proceed if the page doesn't exist
            if rq.status_code != 200:
                print('ER03: Can not connect ({0})\n', tmp_path)
                self.broken_links.add(tmp_path)
                continue

            # Add to my list on new children
            print('    - Child found ({0})', tmp_path)
           # self.child_links.append(tmp_path)

        # END OF FUNC


# You can start NightCrawler from here :)
if __name__ == "__main__":
    try:
        crawler = Crawler(root)
        crawler.start()
    except Exception as e:
        print('Exception: ', e)
