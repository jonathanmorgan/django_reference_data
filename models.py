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
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    
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
        
        return string_OUT

    #-- END __str__() method --#


#-- END class Reference_Domain --#