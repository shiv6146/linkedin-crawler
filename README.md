Linkedin-crawler (Basic)
================

This is a custom crawler that tries to crawl basic info of employees from any given company.

This crawler tries to login to your Linkedin profile, and then tries to search for any given company and recursively
searches the employees from that company.

It returns only the very basic info of the employees, such as their name, location, designation, education.

Requirements
============
1. Python 2.7
2. BeautifulSoup

Steps
=====
1. Clone the repository into your local machine
2. Run the linkedin.py script
3. Enter your linkedin username and password
4. Enter the name of the company and number of employee details to be crawled from the company

Note
====
It is a very basic crawler that might be unstable at times as it doesnot use any Linkedin API
