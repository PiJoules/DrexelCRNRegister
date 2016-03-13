#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script for registering for a class on drexel one.
"""

from __future__ import print_function

from selenium import webdriver
from bs4 import BeautifulSoup


# URL to select the term.
BASE = "https://bannersso.drexel.edu/ssomanager/c/SSB?pkg=bwszkfrag.P_DisplayFinResponsibility%3Fi_url%3Dbwskfreg.P_AltPin"


class RegistrationError(object):
    """Wrapper class for a parsed registration error."""

    __slots__ = ("status", "crn", "subject", "course", "section", "level",
                 "credits", "grade_mode", "title")

    def __init__(self, *args):
        assert len(args) == len(self.__slots__)
        for i in xrange(len(self.__slots__)):
            attr = self.__slots__[i]
            setattr(self, attr, args[i])

    @classmethod
    def from_bs4_elem_tag(cls, elem):
        """Create a reg err from a beautiful soup 4 element tag."""
        td_elems = elem.find_all("td")
        return cls(*[x.text.strip() for x in td_elems])

    def __str__(self):
        return str({attr: getattr(self, attr) for attr in self.__slots__})


def register(username, password, crns):
    """
    Register a user for classes given a list of crns.

    username:
        Drexel id matching [a-z]{2,3}\d{2,3}
    password:
        Drexel login password
    crns:
        List of crns as strings

    return:
        List of RegistrationError objects. Empty list means successful
        registration for all crns provided.
    """
    # Create browser.
    # Use PhantomJS since we don't need to render any html.
    browser = webdriver.PhantomJS()

    # Navigate to SELECT TERM page.
    # We will first be directed to the login page, but redirected to the
    # intended page after successful login.
    browser.get(BASE)

    # Get login elements.
    username_elem = browser.find_element_by_id("username")
    password_elem = browser.find_element_by_id("password")

    # Set login params.
    username_elem.send_keys(username)
    password_elem.send_keys(password)

    # Click submit.
    browser.find_element_by_name("submit").click()

    # We have now been redirected to SELECT TERM page.
    # The first term selected by default is the Quarter (not Semester).
    # Just need to submit since latest quarter is selected.
    browser.find_element_by_css_selector("input[type=submit][value=Submit]").click()

    # Add the crns to the inputs.
    # They follow the pattern "crn_id\d" with a max of 10 inputs.
    for i in xrange(min(10, len(crns))):
        crn = crns[i]
        elem = browser.find_element_by_id("crn_id" + str(i + 1))
        elem.send_keys(crn)

    # Submit crns
    browser.find_element_by_css_selector("input[name=REG_BTN][value='Submit\ Changes'][type=submit]").click()

    # Parse resulting html statuses/errors
    html = browser.page_source

    # Check for registration errors
    if "Registration Add Errors" in html:
        # Registration errors are in datadisplaytable.
        # First row is table header.
        soup = BeautifulSoup(html, "html.parser")
        attrs = {
            "summary": "This layout table is used to present Registration Errors.",
            "class": "datadisplaytable"
        }
        error_elems = soup.find(**attrs).find_all("tr")[1:]
        errors = [RegistrationError.from_bs4_elem_tag(tag) for tag in error_elems]
    else:
        # No errors
        errors = []

    # Quit browser
    browser.quit()

    return errors

