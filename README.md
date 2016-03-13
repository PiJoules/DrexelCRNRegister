# Drexel Class Register
Module for registering for drexel classes.

Note there is no error checking for any of this, so do not use it on any sort of production.
Errors may be thrown do due loss of/poor internet connection or changes in the html.
This script was created on 20160312 and is not guaranteed to work afterwards.

This module works using [Selenium with Python](http://selenium-python.readthedocs.org/) to navigate through the [PhantomJS](http://phantomjs.org/) browser.
Selenium allows for programatic manipulation of a browser at the cost of actually opening the browser and rendering html.
PhantomJS comes into play because it is a gui-less browser, so no html has to be displayed or rendered.


## Dependencies
- Selenium
- PhantomJS
- beautifulsoup4


## Setup
Both the Selenium module for python and beautifulsoup4 cna be installed via pip, but PhantomJS requires that nodejs and npm be installed.

### Environment
The setup instructions may only work for my environment since I have downloaded/installed a version of nodejs and npm for my os specifically.
The version of Phantomjs installed is also prebuilt for this particular os.

This was run and tested on a 32-bit, Ubuntu 14.04 OS.


### Nodejs and phantomjs
```sh
$ curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -  # Node v4 setup
$ sudo apt-get install nodejs-legacy  # node install
$ sudo apt-get instal -y npm  # npm install
$ sudo npm -g install phantomjs-prebuilt  # phantomjs install
```

### Python dependencies
```sh
$ virtualenv venv  # create virtualenv
$ source venv/bin/activate  # activate venv
(venv) $ pip instal -r requirements.txt  # get beautifulsoup4 and selenium
```

At this point, you can add `from register import register` to a python script and call `register()` with your drexel id, password, and list of crns as strings.
```py
from register import register
errors = register("abc123", "mypassword", ["12345", "67890", "34941"])
print(errors)
```

`register()` returns a list of `RegistrationError` objects that describe any errors found upon registering.
No registrationerrors means all crns were submitted successfully.

