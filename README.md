Linkedin-crawler (Basic)
================

This is a custom crawler that tries to crawl basic info of employees from any given company.

This crawler tries to login to your Linkedin profile, and then tries to search for any given company and recursively
searches the employees from that company.

It returns only the very basic info of the employees, such as their name, location, designation, education.

Its been written in Python with the help of BeautifulSoup to parse the DOM and json module to extract and then parse it.
