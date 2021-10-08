# This code taken from https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python
# Sorry I'm lazy xD

import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession


def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def get_results(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    return response


def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = (
        "https://www.google.",
        "https://google.",
        "https://webcache.googleusercontent.",
        "http://webcache.googleusercontent.",
        "https://policies.google.",
        "https://support.google.",
        "https://maps.google.",
    )

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links


def parse_results(response):

    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:

        item = {
            "title": result.find(css_identifier_title, first=True).text,
            "link": result.find(css_identifier_link, first=True).attrs["href"],
            "text": result.find(css_identifier_text, first=True).text,
        }

        output.append(item)

    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)


print(google_search("JavaScript free learning"))

# [
#     {
#         "title": "Learn JavaScript | Codecademy",
#         "link": "https://www.codecademy.com/learn/introduction-to-javascript",
#         "text": "The concepts covered in these lessons lay the foundation for using JavaScript in any environment. Up Next: After learning JavaScript basics, try applying\xa0...\n\u200eWelcome to Learn JavaScript · \u200eLearn Intermediate JavaScript · \u200eIntroduction · \u200eScope",
#     },
#     {
#         "title": "Start learning JavaScript with our free real time tutorial",
#         "link": "https://www.javascript.com/try",
#         "text": "Start learning JavaScript with our interactive simulator for free. Our easy to follow JavaScript tutorials for beginners will have you coding the basics in\xa0...",
#     },
#     {
#         "title": "JavaScript Tutorial - W3Schools",
#         "link": "https://www.w3schools.com/js/",
#         "text": "Start learning JavaScript now » ... If you try all the examples, you will learn a lot about JavaScript, ... JavaScript is free to use for everyone.\n\u200eJavaScript Introduction · \u200eJavaScript Examples · \u200eJavaScript Functions · \u200eTry it Yourself",
#     },
#     {
#         "title": "Learn JavaScript",
#         "link": "https://learnjavascript.online/",
#         "text": "Learn JavaScript is the easiest, most interactive way to learn & practice modern ... challenges, projects (first 7 chapters) & flashcards for free.",
#     },
#     {
#         "title": "Top Free JavaScript Courses & Tutorials Online - Udemy",
#         "link": "https://www.udemy.com/topic/javascript/free/",
#         "text": "Learn Javascript from top-rated instructors. Find the best online Javascript classes and start coding in Javascript today. Javascript is an object-oriented\xa0...",
#     },
#     {
#         "title": "Learn JavaScript - Free Interactive JavaScript Tutorial",
#         "link": "https://www.learn-js.org/",
#         "text": "learn-js.org is a free interactive JavaScript tutorial for people who want to learn JavaScript, fast.",
#     },
#     {
#         "title": "Learn JavaScript for Free: 13 Online Resources for Every ...",
#         "link": "https://www.fullstackacademy.com/blog/learn-javascript-for-free-13-online-tutorials-resources",
#         "text": "Beginner Javascript Courses · JavaScript for Cats · Codecademy's Intro to JavaScript Track · Fullstack Academy's Intro to Coding · Treehouse's JavaScript Basics.",
#     },
#     {
#         "title": "10 Websites to Learn JavaScript Coding for FREE — Best of Lot",
#         "link": "https://medium.com/javarevisited/my-favorite-free-tutorials-and-courses-to-learn-javascript-8f4d0a71faf2",
#         "text": "10-Jan-2020 — 10 Websites to Learn JavaScript Coding for FREE — Best of Lot · 1. Introduction to JavaScript @ Codecademy · 2. Free JavaScript Tutorials @ Udemy.",
#     },
#     {
#         "title": "Learn to Code — For Free — Coding Courses for Busy People",
#         "link": "https://www.freecodecamp.org/",
#         "text": "Learn to Code — For Free. ... Studying JavaScript as well as data structures and algorithms on freeCodeCamp gave me the skills and confidence I needed to\xa0...",
#     },
# ]
