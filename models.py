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

# python base packages
import datetime

# django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# python_utilities
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.network.http_helper import Http_Helper
from python_utilities.network.network_helper import Network_Helper

# Create your models here.

@python_2_unicode_compatible
class Postal_Code( models.Model ):
    
    '''
    This model is designed based on free data from http://geonames.org,
        specifically the country-by-country tab-delimited files of postal codes.
        The fields are moved around a bit, but all fields in those files are in
        this database table, and if you wanted to, you could import them all.
    - To get these files, go to: http://download.geonames.org/export/dump/
    - For the United States: http://download.geonames.org/export/dump/US.zip
    - There is also a fixture for this model that includes the postal codes for
        the United States, from a geonames file US.zip downloaded most recently
        on July 3, 2013.
    '''
    
    #============================================================================
    # constants-ish
    #============================================================================


    #============================================================================
    # Django model fields
    #============================================================================
    
    country_code = models.CharField( max_length = 255 )
    postal_code = models.CharField( max_length = 255 )
    place_name = models.CharField( max_length = 255, null = True, blank = True )
    admin_name1 = models.CharField( max_length = 255, null = True, blank = True ) # state name for U.S.
    admin_code1 = models.CharField( max_length = 255, null = True, blank = True ) # state abbreviation for U.S.
    admin_name2 = models.CharField( max_length = 255, null = True, blank = True ) # county/province for U.S.
    admin_code2 = models.CharField( max_length = 255, null = True, blank = True ) # county/province ID for U.S.
    admin_name3 = models.CharField( max_length = 255, null = True, blank = True ) # community for U.S.
    admin_code3 = models.CharField( max_length = 255, null = True, blank = True ) # community ID for U.S.
    latitude = models.DecimalField( max_digits = 13, decimal_places = 10 )
    longitude = models.DecimalField( max_digits = 13, decimal_places = 10 )
    lat_long_accuracy = models.CharField( max_length = 255, null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    
    #============================================================================
    # class methods
    #============================================================================


    #============================================================================
    # instance methods
    #============================================================================


    def __str__(self):
        
        # return reference
        string_OUT = ""
        
        # id?
        if ( ( self.id ) and ( self.id != None ) and ( self.id > 0 ) ):
        
            string_OUT += "Postal Code " + str( self.id )
        
        #-- END check to see if id --#
        
        # postal_code
        if( self.postal_code ):
        
            string_OUT += " - " + self.postal_code
        
        #-- END check to see if postal_code --#
        
        # place
        if ( self.place_name ):
        
            string_OUT += " - " + self.place_name
        
        #-- END check to see if place_name --#
        
        # state
        if ( self.admin_name1 ):

            string_OUT += " in " + self.admin_name1
            
        #-- END check to see if state --#
        
        return string_OUT

    #-- END __str__() method --#


#-- END class Postal_Code --#


@python_2_unicode_compatible
class Reference_Domain( models.Model ):
    
    
    #============================================================================
    # constants-ish
    #============================================================================


    DOMAIN_TYPE_NEWS = 'news'
    
    # URL parse return types
    URL_PARSE_RETURN_DOMAIN = "domain"
    URL_PARSE_RETURN_PATH = "path"
    
    # statuses
    STATUS_SUCCESS = "Success!"

    
    #============================================================================
    # Django model fields
    #============================================================================
    
    domain_name = models.CharField( max_length = 255 )
    domain_path = models.CharField( max_length = 255, null = True, blank = True )
    long_name = models.TextField( null = True, blank = True )
    full_url = models.CharField( max_length = 255, null = True, blank = True )
    protocol = models.CharField( max_length = 255, null = True, blank = True )
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
    external_id = models.CharField( max_length = 255, null = True, blank = True )
    guid = models.CharField( max_length = 255, null = True, blank = True )
    is_url_ok = models.BooleanField( blank = True, default = False )
    redirect_status = models.IntegerField( null = True, blank = True )
    redirect_message = models.CharField( max_length = 255, null = True, blank = True )
    redirect_full_url = models.CharField( max_length = 255, null = True, blank = True )
    redirect_protocol = models.CharField( max_length = 255, null = True, blank = True )
    redirect_domain_name = models.CharField( max_length = 255, null = True, blank = True )
    redirect_domain_path = models.CharField( max_length = 255, null = True, blank = True )
    parent = models.ForeignKey( 'self', null = True, blank = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_update = models.DateTimeField( auto_now = True )

    
    #============================================================================
    # instance variables
    #============================================================================


    #============================================================================
    # class methods
    #============================================================================


    @classmethod
    def lookup( cls, source_IN = None, domain_name_IN = None, domain_path_IN = None, description_IN = None, *args, **kwargs ):

        '''
        accepts values for fields that can be used to find a matching domain
           record.  For any whose value is not None, filters on that value.
           Returns ResultSet.
           
        parameters:
        - source_IN - source value to find an exact match for.
        - domain_name_IN - domain name to find an exact match for.
        - domain_path_IN - domain path to find an exact match for.
        - description_IN - domain description field to find an exact match for.
        '''
        
        # return reference
        rs_OUT = None
        
        # declare variables

        # first, get RecordSet.
        rs_OUT = Reference_Domain.objects

        # got a source?
        if source_IN != None:
        
            rs_OUT = rs_OUT.filter( source = source_IN )
            
        #-- END check for source --#
        
        # domain name?
        if domain_name_IN != None:
        
            rs_OUT = rs_OUT.filter( domain_name = domain_name_IN )
            
        #-- END check for domain name --#
                
        # domain path?
        if domain_path_IN != None:
        
            # yes.  Is it "/"?
            if ( domain_path_IN == "/" ):
            
                # just for now, because I changed how I parse domains and paths,
                #    if "/", either match with "/" or "".
                rs_OUT = rs_OUT.filter( models.Q( domain_path = domain_path_IN ) | models.Q( domain_path = "" ) )
            
            else:
            
                # not "/", process normally.
                rs_OUT = rs_OUT.filter( domain_path = domain_path_IN )
                
            #-- END check to see if path is "/" --#
            
        #-- END check for domain path --#
                
        # description
        if description_IN != None:
        
            rs_OUT = rs_OUT.filter( description = description_IN )
            
        #-- END check for description --#
                
        return rs_OUT

    #-- END method lookup() --#


    @classmethod
    def lookup_record( cls, source_IN = None, domain_name_IN = None, domain_path_IN = None, description_IN = None, *args, **kwargs ):

        '''
        accepts values for fields that can be used to find a matching domain
           record.  For any whose value is not None, filters on that value.
           Then, checks to see if one record results.  If yes, returns it.  If
           no (either 0 or > 1), returns None.
           
        parameters:
        - source_IN - source value to find an exact match for.
        - domain_name_IN - domain name to find an exact match for.
        - domain_path_IN - domain path to find an exact match for.
        - description_IN - domain description field to find an exact match for.
        '''
        
        # return reference
        record_OUT = None
        
        # declare variables
        match_rs = None
        match_count = -1

        # first, get RecordSet.
        match_rs = cls.lookup( source_IN = source_IN, domain_name_IN = domain_name_IN, domain_path_IN = domain_path_IN, description_IN = description_IN )

        # count?
        match_count = match_rs.count()
        
        # 1, or not?
        if ( match_count == 1 ):
        
            # there is one.  Return it.
            record_OUT = match_rs.get()
        
        else:
        
            # either 0 or more than one.  return None.
            record_OUT = None
        
        #-- END check to see if one match, or other than one --#
            
        return record_OUT

    #-- END method lookup_record() --#


    @classmethod
    def parse_URL( cls, URL_IN = "", return_type_IN = URL_PARSE_RETURN_DOMAIN, *args, **kwargs ):
        
        # return reference
        value_OUT = ""
        
        # declare variables
        network_helper = None
        
        # make network helper instance 
        network_helper = Network_Helper()

        # see what we've been asked to return
        if ( return_type_IN == cls.URL_PARSE_RETURN_PATH ):
        
            # path  (everything after the domain, including query string, etc.,
            #    not just the path).
            value_OUT = network_helper.parse_URL( URL_IN, Network_Helper.URL_PARSE_RETURN_ALL_AFTER_DOMAIN )
            
        else:
        
            # domain
            value_OUT = network_helper.parse_URL( URL_IN, Network_Helper.URL_PARSE_RETURN_TRIMMED_DOMAIN )
            
        #-- END check to see what we return. --#
        
        return value_OUT
        
    #-- END method parse_URL() --#
    
    
    @classmethod
    def test_URLs( cls, print_details_IN = False, domain_rs_IN = None, *args, **kwargs ):
    
        '''
        Loops over all the domains in the database.  For each, calls the
           test_URL() method on it, then if not success, outputs status.

        parameters:
        - print_details_IN - boolean - defaults to False - if True, outputs details using the print() function.
        - domain_rs_IN - ResultSet you want to process - defaults to None - if None, all domains are processed.  If this is populated, just processes the domains in the result set.

        postconditions: all records in the database will have their URLs checked,
           and so will be updated.
        '''
        
        # declare variables
        domain_rs = None
        domain_count = -1
        domain_counter = -1
        current_domain = None
        current_status = ""
        start_dt = None
        success_count = -1
        error_count = -1
        end_dt = None
        
        start_dt = datetime.datetime.now()
        
        # get list of domains to process.
        if ( ( domain_rs_IN ) and ( domain_rs_IN != None ) ):

            # one passed in.  Use it.
            domain_rs = domain_rs_IN

        else:
        
            # nothing passed in.  Process them all.
            domain_rs = cls.objects.all()
            
        #-- END check to see if result set passed in. --#
        
        domain_count = domain_rs.count()
        
        # loop, calling the test_URL() method on each.
        domain_counter = 0
        success_count = 0
        error_count = 0
        for current_domain in domain_rs:
        
            domain_counter += 1
            
            # call the test_URL() method.
            current_status = current_domain.test_URL()
            
            # Success!?
            if ( current_status != cls.STATUS_SUCCESS ):
            
                # Does status contain "ERROR"?
                if "ERROR" in current_status:

                    # not success - increment error count, then output status.
                    error_count += 1
                    
                else:
                    
                    # not success, but not error.  Likely means no redirect.
                    success_count += 1

                #-- END check to see if error --#

                # print details?
                if ( print_details_IN == True ): 
    
                    print( "- STATUS ( domain " + str( domain_counter ) + " of " + str( domain_count ) + ", ID = " + str( current_domain.id ) + " ) - " + current_status )
                    
                #-- END check to see if we print details. --#

            else:
            
                # success!
                success_count += 1

            #-- END check to see if success. --#
        
        #-- END loop over domains --#
    
        # print details?
        if ( print_details_IN == True ): 

            # a little overview
            end_dt = datetime.datetime.now()
            print( "==> Started at " + str( start_dt ) )
            print( "==> Finished at " + str( end_dt ) )
            print( "==> Duration: " + str( end_dt - start_dt ) )
            print( "==> Success: " + str( success_count ) )
            print( "==> Errors: " + str( error_count ) )
                        
        #-- END check to see if we print details. --#

    #-- END method test_URLs() --#


    #============================================================================
    # instance methods
    #============================================================================


    def parse_and_store_URL( self, URL_IN = "", is_redirect_IN = False, *args, **kwargs ):
        
        '''
        Accepts a URL.  Parses it, places the components in nested django fields.
           Returns the trimmed domain name.
        '''
        
        # return reference
        value_OUT = ""
        
        # declare variables
        network_helper = None
        trimmed_domain = ""
        path = ""
        protocol = ""
        params = ""
        query_string = ""
        domain_path = ""
        
        # make network helper instance 
        network_helper = Network_Helper()

        # Got a URL?
        if ( ( URL_IN ) and ( URL_IN != None ) and ( URL_IN != "" ) ):
        
            # yes - use call to get domain to parse URL.
            trimmed_domain = network_helper.parse_URL( URL_IN, Network_Helper.URL_PARSE_RETURN_TRIMMED_DOMAIN )
            
            # get path (everything after the domain, not just the path).
            path = network_helper.parse_URL( URL_IN, Network_Helper.URL_PARSE_RETURN_ALL_AFTER_DOMAIN, use_last_parse_result = True )
            
            # get parse result for the rest.
            parse_result = network_helper.latest_parse_result

            # protocol
            protocol = parse_result.scheme

            # is this a redirect URL?
            if ( is_redirect_IN == True ):
            
                # redirect - store in redirect fields.
                self.redirect_domain_name = trimmed_domain
                self.redirect_domain_path = path
                self.redirect_full_url = URL_IN
                self.redirect_protocol = protocol

            else:
            
                # not redirect - store in redirect fields.
                self.domain_name = trimmed_domain
                self.domain_path = path
                self.full_url = URL_IN
                self.protocol = protocol

            #-- END check to see where we store the values. --#
            
            # return trimmed domain.
            value_OUT = trimmed_domain
            
        else:
        
            # domain
            value_OUT = ""
            
        #-- END check to see what we return. --#
        
        return value_OUT
        
    #-- END method parse_and_store_URL() --#


    def test_URL( self, *args, **kwargs ):
        
        '''
        Retrieves the full URL from the current instance.  Uses the urllib2
           library to load the page.  If the page loads, sets the is_url_ok flag
           to true.  Uses the results of the page load to see if there was a
           redirect (status of 301 or 302).  If so, parses and stores information
           on the final URL that was loaded in the redirect_* fields in this
           object.  Returns a status message that starts with the OK flag, then
           describes whether a redirect occurred, and if so, where the redirect
           went.
           
        Preconditions:
        - must have loaded data into this instance from a row in the database.
        '''
        
        # return reference
        status_OUT = ""
        
        # declare variables
        me = "test_URL"
        http_helper = None
        url_to_test = ""
        redirect_url = ""
        redirect_status_list = ""
        redirect_status_count = -1
        last_redirect_status = -1
        exception_helper = None
        exception_message = ""
        exception_status = ""
        
        # create HTTP Helper
        http_helper = Http_Helper()
        
        # get URL.
        url_to_test = self.full_url
        
        # got a full URL?
        if ( ( not url_to_test ) or ( url_to_test == None ) or ( url_to_test == "" ) ):
        
            # no.  Make one out of domain.
            url_to_test = "http://" + self.domain_name
            
            # got a path?
            if ( ( self.domain_path ) and ( self.domain_path != None ) and ( self.domain_path != "" ) ):
            
                # yes.  Append it, as well.
                url_to_test += self.domain_path
            
            #-- END check to see if domain path. --#
        
        #-- END check to see if URL --#
        
        # now, see if we have a URL again.
        if ( ( url_to_test ) and ( url_to_test != None ) and ( url_to_test != "" ) ):
        
            # try/except to capture problems with URL not resolving at all.
            try:
            
                # we have a URL.  Use the HTTP helper to test.
                redirect_url = http_helper.get_redirect_url_mechanize( url_to_test )
                
                # see if there is a status code.
                redirect_status_list = http_helper.redirect_status_list
                redirect_status_count = len( redirect_status_list )
                if ( redirect_status_count > 0 ):
                
                    # yes.  Get latest one (use pop()).
                    last_redirect_status = redirect_status_list.pop()
                
                #-- END check to see if any statuses --#
                
                # got anything back?
                if ( ( redirect_url ) and ( redirect_url != None ) and ( redirect_url != "" ) ):
                
                    # yes.  Update the record.
                    
                    # URL is OK.
                    self.is_url_ok = True
                    
                    # store HTTP status code.
                    self.redirect_status = last_redirect_status
                    
                    # store full URL.
                    self.redirect_full_url = redirect_url
                    
                    # parse and store components of URL.
                    self.parse_and_store_URL( URL_IN = redirect_url, is_redirect_IN = True )
                    
                    # set status to Success!
                    status_OUT = self.STATUS_SUCCESS

                else:
                
                    # no.  No exception, not redirect.  Just a normal URL.
                    self.is_url_ok = True
                    
                    # set status
                    status_OUT = "Attempt to find redirect returned no URL.  Test URL = " + url_to_test
                    
                    # got a status?
                    if ( ( last_redirect_status ) and ( last_redirect_status > 0 ) ):
                    
                        # there is one.  Append it to message.
                        status_OUT += "; HTTP status code: " + str( last_redirect_status )
                    
                    #-- END check to see if HTTP status code --#
                
                #-- END check to see if redirect URL --#
                
            except Exception as e:
            
                # likely URL not found.  URL is not OK, do nothing else.
                self.is_url_ok = False
                
                # URLError (and child HTTPError) will have a "reason".
                if hasattr( e, 'reason' ):
                
                    # yes.  Store it in the redirect_message field.
                    self.redirect_message = e.reason
                    
                #-- END check to see if "reason" --#

                # HTTPError will have an HTTP status "code".
                if hasattr( e, 'code' ):
                    
                    # yes, store it in the redirect_status field.
                    self.redirect_status = e.code
                    
                #-- END check to see if there is a code.
                
                # make exception helper class.
                exception_helper = ExceptionHelper()
                
                # process the exception
                exception_message = "ERROR - Exception caught in " + me + " trying to resolve URL " + url_to_test + "."
                exception_status = exception_helper.process_exception( exception_IN = e, message_IN = exception_message, print_details_IN = False )
                
                # set status to description of exception
                status_OUT = exception_helper.last_exception_details
            
            #-- END try/except to deal with unknown domains/URLs. --#
            
            # save the results.
            self.save()
        
        else:
        
            status_OUT = "ERROR - Could not find a URL to test for this record."
        
        #-- END check to make sure we have a URL --#
        
        return status_OUT
        
    #-- END method test_URL() --#


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