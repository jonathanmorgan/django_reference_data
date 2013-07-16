# imports

# python base libraries
import datetime
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
import python_utilities.beautiful_soup.beautiful_soup_helper
from python_utilities.strings.string_helper import StringHelper

# django_reference_data
import django_reference_data.models

#===============================================================================#
# declare variables
#===============================================================================#

do_update_existing = True

# constants-ish
BOLD_CONTENTS_CLICK = "Click"
NEWS_MATCH = "news"
TALK_MATCH = "talk"
ELEMENT_NAME_B = "b"
ELEMENT_NAME_A = "a"

# helpers
bs_helper = None

# tracking performance
start_dt = None
end_dt = None
state_counter = -1
station_counter = -1
news_station_counter = -1
domain_counter = -1
error_counter = -1
my_exception_helper = None

# processing state list.
state_list_url = ""
state_list_html = None
state_list_bs = None
data_box_div_list = None
state_list_div = None
state_a_list = None
states_to_process_list = []
state_name = ""
state_url = ""

# only process certain states
# skip 'Texas'.
#states_to_process_list = [ 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'American Samoa', 'Federated States of Micronesia', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 'US Virgin Islands' ]
#states_to_process_list = [ 'Massachusetts', ]

# processing a state's page.
state_html = None
state_bs = None
data_box_div_list = None
station_list_div = None
station_list_container = None

# using bold tags to delimit stations
city_bold_list_bs = None
current_bold_bs = None

# walking through a station's elements.
is_text = False
is_comment = False
a_list_bs = None
text_list_bs = None
keep_strolling = True
last_station_element_bs = None
current_station_element_bs = None
current_element_name = ""
current_element_text = ""
station_text = ""
url_anchor_bs = None

# declare variables - meta-data for each station
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True
source = "http://www.usnpl.com/index_radio.php"

# fields we collect per domain.
station_city = ""
station_call_sign = ""
station_state = ""
station_state_abbreviation = ""
station_url = ""
station_description = ""
cleaned_url = ""
station_domain_name = ""
station_domain_path = ""

#===============================================================================#
# Code
#===============================================================================#

# capture start datetime
start_dt = datetime.datetime.now()

# init beautiful soup helper
bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# first, pull in list of state pages on this site.
state_list_url = "http://www.usnpl.com/index_radio.php"
state_list_html = urllib2.urlopen( state_list_url )

# create beautifulsoup instance for state list.
#bs_parser = "html.parser"
#bs_parser = "lxml"
bs_parser = "html5lib"
#bs_parser = "xml"
state_list_bs = BeautifulSoup( state_list_html, bs_parser )

# get list of state URLs.

# first, get first <div id="data_box">
data_box_div_list = state_list_bs.find_all( "div", id = "data_box" )
state_list_div = data_box_div_list[ 0 ]

# get list of all <a> inside
state_a_list = state_list_div.find_all( "a" )

# initialize variables
state_counter = 0
station_counter = 0
news_station_counter = 0 
domain_counter = 0

# loop over states, opening up each's page and processing newspapers within.
for state_a in state_a_list:

    # increment state counter
    state_counter += 1

    # get values
    state_name = state_a.get_text()
    state_url = state_a[ 'href' ]
    state_abbreviation = state_url[ 27 : 29 ]
    state_abbreviation = state_abbreviation.upper()
    
    # process this state?
    if ( ( len( states_to_process_list ) == 0 ) or ( ( len( states_to_process_list ) > 0 ) and ( state_name in states_to_process_list ) ) ):

        # print next state:
        print( "==> processing " + state_name + " ( " + state_abbreviation + " ) : " + state_url )
        
        # load the state's URL
        state_html = urllib2.urlopen( state_url )
        
        # let BeautifulSoup parse it.
        #bs_parser = "html.parser"
        #bs_parser = "lxml"
        #bs_parser = "html5lib"
        #bs_parser = "xml"
        state_bs = BeautifulSoup( state_html, bs_parser )
        
        # print( state_bs )
        
        # get list of data_boxes.
        data_box_div_list = state_bs.find_all( "div", id = "data_box" )
        
        # get div that contains station list
        station_list_div = data_box_div_list[ 1 ]
        
        # inside that <div> is an entire HTML document - get body.
        #station_list_container = station_list_div.html.body
        station_list_container = station_list_div

        # get all bold tags
        city_bold_list_bs = station_list_container.find_all( "b" )
        
        # loop over <b> tags.
        for current_bold_bs in city_bold_list_bs:
        
            # check to make sure that this isn't one of the "Click" labels at the
            #   top of the list.
            bold_text = current_bold_bs.get_text()
            if ( bold_text.lower() != BOLD_CONTENTS_CLICK.lower() ):
        
                # increment station counter
                station_counter += 1
                
                # initialize
                keep_strolling = True
                a_list_bs = []
                text_list_bs = []
                station_text = ""

                # start out with "last" station = bold tag.
                last_station_element_bs = current_bold_bs

                # walk through adjoining elements until we encounter next <b>.
                while keep_strolling == True:
                
                    # initialize
                    current_element_name = ""
                    current_element_text = ""
                    is_text = False
                    is_comment = False
                    
                    # get next sibling
                    current_station_element_bs = last_station_element_bs.next_sibling
                    last_station_element_bs = current_station_element_bs
                    
                    # got anything at all?
                    if ( ( current_station_element_bs ) and ( current_station_element_bs != None ) ):
                    
                        # is it text?
                        is_text = bs_helper.bs_is_navigable_string( current_station_element_bs )
                        is_comment = bs_helper.bs_is_comment( current_station_element_bs )
                        if ( ( is_text == False ) and ( is_comment == False ) ):
                        
                            # Get element name.
                            current_element_name = current_station_element_bs.name
                            
                            # Is it a <b> tag?
                            if ( current_element_name.lower() == ELEMENT_NAME_B.lower() ):
                            
                                # it is.  This is start of next station. Stop
                                #    strolling.
                                keep_strolling = False
                        
                            # else, is it an <a> tag?
                            elif ( current_element_name.lower() == ELEMENT_NAME_A.lower() ):
    
                                # it is.  Add it to anchor list.
                                a_list_bs.append( current_station_element_bs )
    
                            #-- END check to see if these are elements we care about. --#
                        
                        else:
                        
                            # text - get value, remove parens, strip.  If
                            #    anything left, add to string list.
                            current_element_text = unicode( current_station_element_bs )
                            current_element_text = current_element_text.replace( "(", "" )
                            current_element_text = current_element_text.replace( ")", "" )
                            current_element_text = current_element_text.strip()
                            
                            if ( current_element_text != "" ):

                                # not a paren around a link.  Add to list.
                                text_list_bs.append( current_element_text )
                                
                            #-- END check to see if clean string is populated. --#
                        
                        #-- END check to see if text --#
                        
                    else:
                    
                        # None - no next element.  stop walking.
                        keep_strolling = False
                    
                    #-- END check to see if there is a next element. --#
                
                #-- END loop over station elements. --#

                #print( a_list_bs )
                #print( text_list_bs )
                
                # make a string out of the text.
                station_text = " ".join( text_list_bs )
                
                # clean string - strip out newlines, tabs, and more than one
                #    contiguous space.
                station_text = StringHelper.clean_string( station_text )
                
                # is this a news station?
                # Either:
                # - contains the word "news"
                # - contains "talk", but not "sport", "christian", or "religious" (I checked the sites that match these by hand, they don't have news).
                if ( ( NEWS_MATCH.lower() in station_text.lower() ) or ( ( TALK_MATCH.lower() in station_text.lower() ) and ( ( "sport" not in station_text.lower() ) and ( "christian" not in station_text.lower() ) and ( "religious" not in station_text.lower() ) ) ) ):
                
                    # news!
                    news_station_counter += 1
                    
                    print( "- NEWS: " + bold_text + " - " + station_text )
                    
                    # get URL.  Got anything in <a> list?
                    if ( len( a_list_bs ) > 0 ):
                    
                        # yes - get anchor element
                        url_anchor_bs = a_list_bs[ 0 ]
                        
                        # get URL and call sign
                        station_url = url_anchor_bs[ "href" ].strip()
                        station_call_sign = url_anchor_bs.get_text().strip()
                        
                    #-- END check to see if anything in <a> list.

                    # Get more information on station, make description.
                    station_state = state_abbreviation
                    station_city = bold_text
                    station_description = station_city + ", " + station_state + " - " + station_call_sign + " - " + station_text

                    # do we have a URL?
                    if ( ( station_url ) and ( station_url != None ) and ( station_url != "" ) ):

                        # yes - adding to database.
                        domain_counter += 1
                        print( "    ===> processing station: " + station_description )
        
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
                        current_source_details = state_url
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
                        #current_domain_instance.address = station_address
                        current_domain_instance.state = station_state
                        #current_domain_instance.county = ""
                        current_domain_instance.city = station_city
                        #current_domain_instance.zip_code = station_zip_code
                        #current_domain_instance.phone = station_phone
                        #current_domain_instance.fax = station_fax
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
                
                    # not news.
                    print( "- NON-NEWS: " + bold_text + " - " + station_text )
                
                #-- END check to see if news. --#
    
            else:
            
                # not a station...
                print( "- bold \"Click\" found.  Moving on." )

            #-- END check to see if this is a station --#
        
        #-- END loop over bold tags --#
        
    else:
    
        # print next state:
        print( "==> skipping " + state_name + " ( " + state_abbreviation + " ) : " + state_url ) 
    
    #-- END check to see if we proces this state. --#

#-- END loop over states in state list --#

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> States: " + str( state_counter ) )
print( "==> Stations: " + str( station_counter ) )
print( "==> News Stations: " + str( news_station_counter ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> Errors: " + str( error_counter ) )