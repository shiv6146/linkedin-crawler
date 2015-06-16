import cookielib
import os
import urllib2
import urllib
import re
import json_extractor #Custom written module, that extracts JSON from the DOM
import BeautifulSoup
import getpass

username = raw_input("Enter your linkedin username : ")
password = getpass.getpass("Enter your linkedin password : ")

cookie_filename = "parser.cookies.txt" #Cookies set by linkedin are stored
dom_filename="dom.txt" #The entire DOM of the page currently viewed is stored
path=os.path.split(__file__)[0]

class LinkedInParser(object):

    def __init__(self, login, password):
        if(os.path.isfile(os.path.join(path,cookie_filename))):
            os.remove(os.path.join(path,cookie_filename))
        """ Start up... """
        self.login = login
        self.password = password

        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]

        # Login
        self.loginPage()

        self.cj.save()


    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        # We'll print the url in case of infinite loop
        # print "Loading URL: %s" % url
        try:
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            return ''.join(response.readlines())
        except:
            # If URL doesn't load for ANY reason, try again...
            # Quick and dirty solution for 404 returns because of network problems
            # However, this could infinite loop if there's an actual problem
            return self.loadPage(url, data)

    def loginPage(self):
        """
        Handle login. This should populate our cookie jar.
        """
        html = self.loadPage("https://www.linkedin.com/")
        soup = BeautifulSoup.BeautifulSoup(html)
        csrf = soup.find(id="loginCsrfParam-login")['value']

        login_data = urllib.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        })

        html = self.loadPage("https://www.linkedin.com/uas/login-submit", login_data)
        return


    def searchCompany(self,name):
        html=self.loadPage("http://www.linkedin.com/vsearch/p?type=people&keywords="+name)
        soup=BeautifulSoup.BeautifulSoup(html)
        if(os.path.isfile(os.path.join(path,dom_filename))):
            os.remove(os.path.join(path,dom_filename))
        f=open("dom.txt","a")
        f.write(str(soup))
        f.close()

parser = LinkedInParser(username, password) #Creating an instance for LinkedInParser, and the constructor takes in username,password set above as parameters to login

print "Enter company name to search: "
name = raw_input()
print "Enter the required number of employees: "
n=int(raw_input())
parser.searchCompany(name) #This loads the search page with list of matching company and writes the entire page source to file "dom.txt"
d=json_extractor.returnDetails(name,n) #Since, the page has dynamic links its impossible to parse the DOM to get through, so this extracts the JSON from "dom.txt" and then parses it

for i in d:
    print d[i][0]
    for j in range(1,len(d[i])):
        print d[i][j]
    print '*'*100
