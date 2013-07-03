from __future__ import unicode_literals

'''
Copyright 2013 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/django_reference_data.

django_reference_data is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

django_reference_data is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with http://github.com/jonathanmorgan/django_reference_data.  If not, see
<http://www.gnu.org/licenses/>.
'''

# imports

# django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

# !TODO abstract parent class, since just about everything is identical between these.

@python_2_unicode_compatible
class Reference_Domain( models.Model ):
    
    
    #============================================================================
    # constants-ish
    #============================================================================


    DOMAIN_TYPE_NEWS = 'news'
    
    # URL parse return types
    URL_PARSE_RETURN_DOMAIN = "domain"
    URL_PARSE_RETURN_PATH = "path"

    
    #============================================================================
    # Django model fields
    #============================================================================
    
    domain_name = models.CharField( max_length = 255 )
    domain_path = models.CharField( max_length = 255, null = True, blank = True )
    long_name = models.TextField( null = True, blank = True )
    description = models.CharField( max_length = 255, null = True, blank = True )
    source = models.CharField( max_length = 255, null = True, blank = True )
    source_details = models.CharField( max_length = 255, null = True, blank = True )
    domain_type = models.CharField( max_length = 255, null = True, blank = True )
    is_news = models.BooleanField( blank = True, default = False )
    is_multimedia = models.BooleanField( blank = True, default = False )
    rank = models.IntegerField( null = True, blank = True )
    address = models.CharField( max_length = 255, null = True, blank = True )
    state = models.CharField( max_length = 255, null = True, blank = True )
    county = models.CharField( max_length = 255, null = True, blank = True )
    city = models.CharField( max_length = 255, null = True, blank = True )
    zip_code = models.CharField( max_length = 255, null = True, blank = True )
    email = models.CharField( max_length = 255, null = True, blank = True )
    phone = models.CharField( max_length = 255, null = True, blank = True )
    fax = models.CharField( max_length = 255, null = True, blank = True )
    label = models.CharField( max_length = 255, null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    
    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def parse_URL( cls, URL_IN = "", return_type_IN = URL_PARSE_RETURN_DOMAIN, *args, **kwargs ):
        
        # return reference
        value_OUT = ""
        
        # declare variables
        domain_name = ""
        slash_index = -1
        url_path = ""
        
        # place the URL in domain_name
        domain_name = URL_IN
        
        # strip off https://
        domain_name = domain_name.replace( "https://", "" )
        
        # strip off http://
        domain_name = domain_name.replace( "http://", "" )
        
        # strip off www.
        domain_name = domain_name.replace( "www.", "" )
        
        # normal domaindomain path?
        slash_index = domain_name.find( "/" )
        if ( slash_index >= 0 ):
        
            # there is path information in domain.  Take string from "/" to end,
            #    store it as domain path.  Take string up to but not including
            #    the "/", keep that as domain.
            url_path = domain_name[ slash_index : ]
            domain_name = domain_name[ : slash_index ]
        
        else:
        
            # no slashes - make sure path is empty.
            url_path = ""
        
        #-- END check to see if path information. --#
        
        # is path just "/"?  If so, set to "".
        if ( url_path == "/" ):
        
            # yup. Set to "".
            url_path = ""
        
        #-- END check to see if path is just "/" --#
        
        # see what we've been asked to return
        if ( return_type_IN == cls.URL_PARSE_RETURN_PATH ):
        
            # path
            value_OUT = url_path
            
        else:
        
            # domain
            value_OUT = domain_name
            
        #-- END check to see what we return. --#
        
        return value_OUT
        
    #-- END method parse_URL() --#
    


    #============================================================================
    # instance methods
    #============================================================================


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "Domain " + str( self.id )
        
        #-- END check to see if id --#
        
        # name
        if( self.domain_name ):
        
            string_OUT += " - " + self.domain_name
        
        #-- END check to see if domain_name --#
        
        # description
        if ( self.description ):
        
            string_OUT += " - " + self.description
        
        #-- END check to see if description --#
        
        # source
        if ( self.source ):

            string_OUT += " ( from: " + self.source + " )"
            
        #-- END check to see if source --#
        
        return string_OUT

    #-- END __str__() method --#


#-- END class Reference_Domain --#