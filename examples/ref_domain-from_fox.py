'''
Will need to do some manual cleanup after you run this script.  Couldn't write
   it so it dealt with all the inconsistencies in the HTML.  In particular, look
   for places where address area is non-standard (multiple telephone numbers,
   etc.).  URL/domain/path collection doesn't seem to be affected.
'''

# imports

# python base libraries
import urllib2
import re

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
import python_utilities.beautiful_soup.beautiful_soup_helper
from python_utilities.strings.string_helper import StringHelper

# django_reference_data
import django_reference_data.models

# constants-ish
COMMENT_STATE_CONTAINS = "STATE"
COMMENT_STATION_CONTAINS = "STATION INFORMATION ROW"
URL_FORWARD_STRING = ""

PHONE_PREFIX = "(V)"
FAX_PREFIX = "(F)"

#===============================================================================#
# declare variables
#===============================================================================#

do_update_existing = True
bs_helper = None
page_list = []
page_counter = -1
page_url = ""
page_html = ""
page_bs = None

# declare variables - parsing HTML
page_dd_list_bs = None
station_dd_bs = None
station_counter = -1
station_anchor_bs = None
link_text = ""
dd_string_list_bs = None
station_text_list = []
is_text = False
dd_child_bs = None
temp_text = ""
phone_index = -1

# dealing with remaining address lines
address_line_index = -1
address_line_text = ""

# declare variables - meta-data for each station
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True
source = "http://www.fox.com/affiliates.php"

# declare variables - grabbing station data.
station_text_list = []
station_city = ""
station_call_sign = ""
station_address = ""
station_state = ""
station_state_abbreviation = ""
station_zip_code = ""
station_phone = ""
station_fax = ""
station_email = ""
station_url = ""
station_description = ""
cleaned_url = ""
station_domain_name = ""
station_domain_path = ""

# parsing city, state, zip
city_state_zip_string = ""
city_index = -1
city_state_zip_item_list = []

# declare variables - store in database.
current_domain_instance = None

# make instance of BeautifulSoupHelper
bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# create list of pages we need to parse.
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_north-east.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_mid_east.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_south_east.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_central.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_mountain.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_pacific.php" )
page_list.append( "http://www.fox.com/_inc/affiliates/affiliates_details_other.php" )

#===============================================================================#
# Code
#===============================================================================#

# loop over pages
page_counter = 0
for page_url in page_list:

    print( "Current Page: " + page_url )

    # load the page.
    page_html = urllib2.urlopen( page_url )

    # create beautifulsoup instance for state list.
    #bs_parser = "html.parser"
    #bs_parser = "lxml"
    bs_parser = "html5lib"
    page_bs = BeautifulSoup( page_html, bs_parser )

    # get all <dd> elements on page (these are the two columns of stations in the
    #    station list).
    page_dd_list_bs = page_bs.find_all( "dd" )
    
    # Loop over these elements.
    station_counter = 0
    for station_dd_bs in page_dd_list_bs:

        # increment station_counter
        station_counter += 1
        
        # clear out variables
        station_text_list = []
        station_city = ""
        station_call_sign = ""
        station_address = ""
        station_state = ""
        station_state_abbreviation = ""
        station_zip_code = ""
        station_phone = ""
        station_fax = ""
        station_email = ""
        station_url = ""
        station_description = ""
        cleaned_url = ""
        station_domain_name = ""
        station_domain_path = ""
        
        # first, look for <a> element.
        station_anchor_bs = station_dd_bs.find( "a" )
        
        # got anything?
        if ( ( station_anchor_bs ) and ( station_anchor_bs != None ) ):
        
            # yes, we have a link.  First, get URL and text from it.
            station_url = station_anchor_bs[ 'href' ]
            link_text = station_anchor_bs.get_text().strip()
            
            # use link_text as start of description, also parse out call sign and
            #    state postal code.
            station_description = link_text
            station_call_sign = link_text[ : 4 ]
            station_state_abbreviation = link_text[ len( link_text ) - 2 : ]
            
            # then, loop over children, appending all text, trimmed, into a text
            #    list.
            station_text_list = []
            
            # get all strings in the <dd> element.
            dd_string_list_bs = station_dd_bs.stripped_strings
            for dd_child_bs in dd_string_list_bs:
            
                # Add it to our list.
                station_text_list.append( unicode( dd_child_bs ).strip() )
            
            #-- END loop over children of dd element. --#
            
            print( "Station text list: " + str( station_text_list ) )
            
            # last item might be fax, might be phone.  Grab it.
            station_fax = station_text_list.pop()
            
            # process station_fax, set station_phone as well.

            # Does it contain "(F)"? (formatted: "(F)XXX-XXX-XXXX" )
            # fax prefix could be upper case or lower case - account for either.
            if ( FAX_PREFIX.lower() in station_fax.lower() ):
            
                # it is indeed the fax number. strip off the "(F)"
                # fax prefix could be upper case or lower case - account for either.
                station_fax = station_fax.replace( FAX_PREFIX, "" )
                station_fax = station_fax.replace( FAX_PREFIX.lower(), "" )
                
                # pop() next string, store it in station_phone variable.
                station_phone = station_text_list.pop()
            
            else:
            
                # no "(F)" - perhaps it is phone? "(P)"
                # phone prefix could be upper case or lower case - account for either.
                if ( PHONE_PREFIX.lower() in station_fax.lower() ):
                
                    # it is phone.  No fax.  Put value in station_phone, then
                    #    empty station_fax.
                    station_phone = station_fax
                    station_fax = ""
                
                else:
                
                    # yikes.  Not phone or fax.  Error.
                    station_fax = ""
                    station_phone = ""
                
                #-- END check to see if phone or fax. --#
                
            #-- END check to see if fax.

            print( "fax: " + station_fax )
            print( "phone: " + station_phone )

            # then phone
            #station_phone = station_text_list.pop()
            # station_phone now set based on whether there is a fax number.
            
            # get phone and city-state-zip values (phone might be on same line
            #    as city-state-zip)
            # phone prefix could be upper case or lower case - account for either.
            phone_index = station_phone.lower().find( PHONE_PREFIX.lower() )
            if ( phone_index > 0 ):
            
                # phone is not the first thing in this text.  Likely on the same
                #    line as city-state-zip.  Oy.
                
                # split string into city state zip and phone.
                temp_string = station_phone
                station_phone = temp_string[ phone_index : ]
                city_state_zip_string = temp_string[ : phone_index ]
                
            elif ( phone_index == 0 ):
            
                # this is phone.  pop() next line to get city_state_zip_string.
                city_state_zip_string = station_text_list.pop()
            
            else:
            
                # not a phone number... ERROR - put this in city-state-zip
                #    variable, see what happens next.
                city_state_zip_string = station_phone
            
            #-- END check to see what is in phone line. --#

            print( "phone: " + station_phone )
            print( "city-state-zip: " + city_state_zip_string )
            
            # strip off the "(P)" from station_phone
            # phone prefix could be upper case or lower case - account for either.
            station_phone = station_phone.replace( PHONE_PREFIX, "" )
            station_phone = station_phone.replace( PHONE_PREFIX.lower(), "" )
            
            # see if we have a city_state_zip_string.
            if ( ( city_state_zip_string ) and ( city_state_zip_string != "" ) ):
            
                # we do.  Assume format of <city>, <state> <zip>
                
                # first, split on white space.
                city_state_zip_item_list = city_state_zip_string.split()
                
                # last item should be zip code.
                station_zip_code = city_state_zip_item_list.pop().strip()
                
                # then, put string back together
                temp_text = " ".join( city_state_zip_item_list )
                
                # now, split on space again.
                city_state_zip_item_list = temp_text.split( " " )
            
                # last item should be state.
                station_state = city_state_zip_item_list.pop().strip()

                # put string back together again
                temp_text = " ".join( city_state_zip_item_list )
                
                # this is city.
                station_city = temp_text
                
                # comma in city name?
                if ( "," in station_city ):
                
                    # is it the last character?
                    comma_position = station_city.rfind( "," )
                    if ( comma_position == ( len( station_city ) - 1 ) ):
                    
                        # it is.  Remove last character.
                        station_city = station_city[ : ( len( station_city ) - 1 ) ]
                    
                    #-- END check to see if comma is last thing in city --#
                
                #-- END check for comma in city name. --#
            
            #-- END check to see if city_state_zip_string. --#
            
            # address string - join the rest of the list together, except the
            #    first thing in the list (it is the call sign, etc., from inside
            #    the anchor).
            station_address = ""
            for address_line_index in range( ( len( station_text_list ) -1 ), 0, -1 ):

                # append string to station_address.
                address_line_text = station_text_list[ address_line_index ]
                address_line_text = address_line_text.strip()
                station_address += address_line_text
                
            #-- END loop over remaining address lines (except the first one). --#

            print( "station_address: " + station_address )
            
            # Now, we actually put the information together and store to
            #    database.

            # make station description
            station_description += " - " + station_call_sign + " - " + station_address + "; " + station_city + ", " + station_state + " " + station_zip_code
            
            # clean out new lines
            station_description = StringHelper.clean_string( station_description )
            
            # do we have a URL?
            if ( ( station_url ) and ( station_url != None ) and ( station_url != "" ) ):
            
                # adding to database.
                print( "    ===> adding station: " + station_description )

                # domain name
                cleaned_url = station_url
                
                # handle redirect URLS? - first, see if this URL contains "goto="
                #redirect_index = cleaned_url.find( URL_FORWARD_STRING )
                #if ( redirect_index >= 0 ):
                #    # yes.  strip off everything before "goto="
                #    cleaned_url = cleaned_url[ ( redirect_index + len( URL_FORWARD_STRING ) ) : ]
                #-- END check to see if domain has "goto=" --#

                # parse out domain and path
                station_domain_name = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
                station_domain_path = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )

                # set up meta-data.
                current_source = source
                current_source_details = page_url
                current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
                current_is_news = True
                
                print( "    - Domain: " + station_domain_name + "; path: " + station_domain_path )
                
                # get Reference_Domain instance
                
                # update existing?
                if ( do_update_existing == True ):
    
                    try:
        
                        # first, try looking up existing domain.
                        domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
                        domain_rs = domain_rs.filter( domain_name = station_domain_name )
                        domain_rs = domain_rs.filter( domain_path = station_domain_path )
                        current_domain_instance = domain_rs.get( description = station_description )
                    
                    except:
                    
                        # No matching row.  Create new instance.
                        current_domain_instance = django_reference_data.models.Reference_Domain()
                        
                    #-- END attempt to get existing row. --#
    
                else:
                
                    # not updating.  Just create new instance.
                    current_domain_instance = django_reference_data.models.Reference_Domain()
                
                #-- END check to see if we update existing. --#
                
                # set values
                #current_domain_instance.domain_name = station_domain_name
                #current_domain_instance.domain_path = station_domain_path
                #current_domain_instance.long_name = None

                # parse and store the URL information.
                current_domain_instance.parse_and_store_URL( cleaned_url )

                current_domain_instance.description = station_description
                current_domain_instance.source = current_source
                current_domain_instance.source_details = current_source_details
                current_domain_instance.domain_type = current_domain_type
                current_domain_instance.is_news = current_is_news
                #current_domain_instance.is_multimedia = False
                #current_domain_instance.rank = current_rank
                current_domain_instance.address = station_address
                current_domain_instance.state = station_state
                #current_domain_instance.county = ""
                current_domain_instance.city = station_city
                current_domain_instance.zip_code = station_zip_code
                current_domain_instance.phone = station_phone
                current_domain_instance.fax = station_fax
                # current_domain_instance.email = station_email
                current_domain_instance.label = station_call_sign
        
                # save
                current_domain_instance.save()                    
            
                print( "    - Added: " + str( current_domain_instance ) )
        
            else:
            
                # no URL - not adding to database.
                print( "    ===> no URL: " + station_description )

            #-- END check to see if station_url.
            
        else:
        
            # a <dd> without a link in it - no URL, so moving on.
            print( "===> Found <dd> ( number " + str( station_counter ) + " ) with no link: \"" + station_dd_bs.get_text() + "\";  Moving on." )

        #-- END check to see if anchor --#
    
    #-- END loop over <dd> elements ---#

#-- END loop over pages in page list. --#