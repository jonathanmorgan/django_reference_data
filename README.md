# django\_reference\_data

Django application for accruing reference data that you can use across applications.

## Installation

- install pip

        (sudo) easy_install pip

- install beautiful soup 4

        (sudo) pip install beautifulsoup4

- install django

        (sudo) pip install django

- install South (data migration tool), if it isn't already installed.

        (sudo) pip install South

- in your work directory, create a django site.

        django-admin.py startproject <site_directory>
    
- cd into the site\_directory

        cd <site_directory>
    
- pull in python\_utilities

        git clone https://github.com/jonathanmorgan/python_utilities.git

- pull in the python django\_reference\_data code

        git clone https://github.com/jonathanmorgan/django_reference_data.git
    
### Configure

- from the site\_directory, cd into the site configuration directory, where settings.py is located (it is named the same as site\_directory, but nested inside site\_directory, alongside all the other django code you pulled in from git - <site\_directory>/<same\_name\_as\_site\_directory>).

        cd <same_name_as_site_directory>

- in settings.py, set USE_TZ to false to turn off time zone support:

        USE_TZ = False

- configure the database in settings.py

    - I recommend using PostgreSQL.  That said, I only recently arrived at this recommendation, and so don't haven't really followed it myself, so no detailed doc for it just yet (its unicode support is supposedly a gazillion times better than mysql).

    - For mysql:

        - create mysql database.
            - at the least, make your database use character set utf8 and collation utf8_unicode_ci
            - To support emoji and crazy characters, in mysql >= 5.5.2, you can try setting encoding to utf8mb4 and collation to utf8mb4\_unicode\_ci instead of utf8 and utf8\_unicode\_ci.  It didn't work for me, but I converted the database instead of starting with it like that from scratch, so your mileage may vary.  If you need to do this to an existing database:

                    ALTER DATABASE <database_name> CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

        - create user to interact with mysql database.  Set permissions so user has all permissions to your database.
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.mysql"
            - set the database NAME, USER, and PASSWORD.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': '<db_name>',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': '<db_username>',
                        'PASSWORD': '<db_password>',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }

    - For sqlite3:

        - figure out what file you want to hold the database.  For the initial implementation, we used reddit.sqlite in same directory as code (/home/socs/socs_reddit/reddit_collect/reddit.sqlite).
        - In settings.py, in the DATABASES structure:
            - set the ENGINE to "django.db.backends.sqlite3"
            - set the database NAME (path to file), USER and PASSWORD if you set one on the database.
            - If the database is not on localhost, enter a HOST.
            - If the database is listening on a non-standard port, enter a PORT.
        - Example:

                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                        'NAME': '/home/socs/socs_reddit/reddit_collect/reddit.sqlite',                      # Or path to database file if using sqlite3.
                        # The following settings are not used with sqlite3:
                        'USER': '',
                        'PASSWORD': '',
                        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                        'PORT': '',                      # Set to empty string for default.
                    }
                }


- in settings.py, add 'south' to the INSTALLED\_APPS list.  Example:
    
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Uncomment the next line to enable the admin:
            # 'django.contrib.admin',
            # Uncomment the next line to enable admin documentation:
            # 'django.contrib.admindocs',
            'south',
        )

- Once database is configured in settings.py, in your site directory, run "python manage.py syncdb" to create database tables.

- in settings.py, add 'django\_reference\_data' to the INSTALLED\_APPS list.  Example:
    
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Uncomment the next line to enable the admin:
            # 'django.contrib.admin',
            # Uncomment the next line to enable admin documentation:
            # 'django.contrib.admindocs',
            'south',
            'django_reference_data',
        )

- run `python manage.py migrate django_reference_data`.

## Usage

### Getting started and initialization

The easiest way to run code from a shell is to go to your django sites folder and use manage.py to open a shell:

    python manage.py shell
    
If you choose, you can also just open the base python interpreter:

    python
    
Or you can install something fancier like ipython (`pip install ipython`). or install it using your OS's package manager), and then run ipython:

    ipython
    
If you don't use manage.py to open a shell (or if you are making a shell script that will be run on its own), you'll have to do a little additional setup to pull in and configure django:

    # make sure the site directory is in the sys path.
    import sys
    site_path = '<site_folder_full_path>'
    if site_path not in sys.path:
        
        sys.path.append( site_path )
        
    #-- END check to see if site path is in sys.path. --#
    
    # if not running in django shell (python manage.py shell), make sure django
    #    classes have access to settings.py
    # set DJANGO_SETTINGS_MODULE environment variable = "<site_folder_name>.settings".
    import os
    os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "<site_folder_name>.settings"

### Examples

Then, there are numerous examples in /examples you can use to try out different ways of creating domain reference data (domains are the only type implemented at the moment):

- ref\_domain-from\_alexa.py - pull in domains from alexa's lists of most popular web sites.
- ref\_domain-from\_cbsnews.py - pull in domain names of CBS news' local affiliate stations' web sites.
- ref\_domain-from\_listofnewspapers - pull in domains of newspaper websites in the United States from listofnewspapers.com.

These are good examples of how to use Beautiful Soup 4, also, if you are interested!

There is also a fixture of news domains you can import into the reference\_domain model in /fixtures/reference\_domains\_news.json.  To load it:

        python manage.py loaddata reference_domains_news.json

### Postal Codes

The Postal\_Code model is designed based on free data from [http://geonames.org](http://geonames.org), specifically the country-by-country tab-delimited files of postal codes.  The fields are moved around a bit, but all fields in those files are in this database table, and if you wanted to, you could import them all.

To get these files, go to [http://download.geonames.org/export/dump/](http://download.geonames.org/export/dump/) ( for the United States: [http://download.geonames.org/export/dump/US.zip](http://download.geonames.org/export/dump/US.zip) ).

There is a fixture for this model that includes the postal codes for the United States, from a geonames file US.zip downloaded most recently on July 3, 2013.  It is /fixtures/postal\_codes\_US.json.  To load it:

        python manage.py loaddata postal_codes_US.json

The original tab-delimited file zip archive is also in the respository: /examples/US-ZIP-2012.07.02 (includes readme, tab-delimited postal code file, and that same file converted to Excel).

## License:

Copyright 2012, 2013 Jonathan Morgan

This file is part of [http://github.com/jonathanmorgan/django\_reference\_data](http://github.com/jonathanmorgan/django_reference_data).

django\_reference\_data is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

django\_reference\_data is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [http://github.com/jonathanmorgan/django\_reference\_data](http://github.com/jonathanmorgan/django_reference_data).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).