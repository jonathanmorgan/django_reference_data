'''
Example XML:
<?xml version="1.0" encoding="utf-8"?>
<stations version="0.94">
    <title>Stations near Anderson, AK</title>
    <station id="196">
        <callLetters>KUAC</callLetters>
        <band>FM</band>
        <name>KUAC-FM</name>
        <memberStatus>Member</memberStatus>
        <guid>4fcf700f0ff3472ab41cbfc4daf1a875</guid>
        <frequency>89.9</frequency>
        <marketCity>Fairbanks</marketCity>
        <state>AK</state>
        <signal strength="3">moderate</signal>
        <url title="KUAC-FM Homepage" type="Organization Home Page" typeId="1">http://www.kuac.org/</url>
        <url title="Program Guide" type="Program Schedule" typeId="2">http://www.publicbroadcasting.net/kuac/guide.guidemain</url>
        <url title="Support" type="Pledge Page" typeId="4">http://secure.publicbroadcasting.net/kuac/pledge.pledgemain</url>
        <url title="KUAC-FM (mobile)" type="Audio Stream Landing Page" typeId="7">http://www.kuac.org/kuac-fm/live-stream.html</url>
        <url title="KUAC-FM (broadband)" type="Audio Stream Landing Page" typeId="7">http://www.kuac.org/kuac-fm/live-stream.html</url>
        <url guid="4fcf7140060b48c1911e512a46af6236" primary="true" title="KUAC-FM (mobile)" type="Audio MP3 Stream" typeId="10">http://linux0.cs.uaf.edu/radio/playlists/kuac16mono.m3u</url>
        <url guid="4fcf7140060b48c1911e512a46af6236" primary="true" title="KUAC-FM (broadband)" type="Audio MP3 Stream" typeId="10">http://linux0.cs.uaf.edu/radio/playlists/kuac64stereo.m3u</url>
        <url title="Facebook" type="Facebook Url" typeId="16">http://www.facebook.com/pages/KUAC/132219969921</url>
        <url title="Twitter" type="Twitter Feed" typeId="17">https://twitter.com/KUACFM</url>
        <image type="logo">http://media.npr.org/images/stations/logos/kuac_fm.gif</image>
        <tagline>Public Radio for Alaska's Interior</tagline>
        <orgDisplayName>KUAC</orgDisplayName>
        <identifierAudioUrl type="mp3">http://media.npr.org/stationid/196.mp3</identifierAudioUrl>
        <identifierAudioUrl type="mp4">http://media.npr.org/stationid/196.mp4</identifierAudioUrl>
    </station>
    <station id="5130968">
        <callLetters>KUAC</callLetters>
        <band>FM</band>
        <name>KUAC-FM</name>
        <memberStatus>Translator</memberStatus>
        <guid>503e27ba13404988a14a0054d7db1c11</guid>
        <frequency>91.1</frequency>
        <translator_callLetters>K216AN</translator_callLetters>
        <translator_band>FX</translator_band>
        <network orgId="196">KUAC-FM</network>
        <marketCity>Fairbanks</marketCity>
        <state>AK</state>
        <signal strength="1">weak</signal>
        <image type="logo">http://media.npr.org/images/stations/logos/kuac_fm.gif</image>
        <tagline>Public Radio for Alaska's Interior</tagline>
        <orgDisplayName>KUAC</orgDisplayName>
    </station>
    <station id="816">
        <callLetters>KYUK</callLetters>
        <band>AM</band>
        <name>KYUK-AM</name>
        <memberStatus>Non-Member - GF</memberStatus>
        <guid>4fcf701308d9468f94ea0689e74d33a4</guid>
        <frequency>640</frequency>
        <marketCity>Bethel</marketCity>
        <state>AK</state>
        <signal strength="1">weak</signal>
        <url title="KYUK Homepage" type="Organization Home Page" typeId="1">http://kyuk.org/category/radio/</url>
        <url title="Program Schedule" type="Program Schedule" typeId="2">http://kyuk.org/category/radio/</url>
        <url title="Support" type="Pledge Page" typeId="4">http://kyuk.org/pledge-to-kyuk-win-prizes-feel-good/</url>
        <url title="KYUK English News" type="Audio Stream Landing Page" typeId="7">http://www.kyuk.org</url>
        <url guid="4fcf71601898449e9eda3fd418e6a160" primary="true" title="KYUK English News" type="Audio MP3 Stream" typeId="10">http://www.publicbroadcasting.net/kyuk/ppr/kyuk.m3u</url>
        <image type="logo">http://media.npr.org/images/stations/logos/kyuk_am.gif</image>
        <tagline>Bethel Broadcasting</tagline>
        <orgDisplayName>KYUK</orgDisplayName>
    </station>
</stations>
'''
# imports

# python base libraries
import datetime
import re
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
import python_utilities.beautiful_soup.beautiful_soup_helper
from python_utilities.database.MySQLdb_helper import MySQLdb_Helper
from python_utilities.exceptions.exception_helper import ExceptionHelper

# django_reference_data
import django_reference_data.models

#===============================================================================#
# declare variables
#===============================================================================#

# constants-ish
do_update_existing = True
source = "NPR Station Finder API"
source_API_URL = "http://api.npr.org/stations"
source_detail = ""

# debugging
debug_flag = False

# declare variables
db_host = ""
db_port = -1
db_username = ""
db_password = ""
db_database = ""
db_helper = None
db_connection = None
db_read_cursor = None
select_sql = ""

# tracking performance
start_dt = None
end_dt = None
city_counter = -1
domain_counter = -1
no_match_counter = -1
error_counter = -1
my_exception_helper = None

# cities from database.
current_row = None
current_city = ""
current_state = ""
current_city_encoded = ""

# station finder API
my_api_key = ""
npr_url = ""
npr_xml = None
npr_bs = None

# NPR XML
message_list_bs = None
station_list_bs = None
current_station_bs = None
temp_element = None

# API status/error messages
current_message = None
message_id = ""
message_level = ""
message_text = ""

# station information
station_id = ""
station_call_letters = ""
station_band = ""
station_name = ""
station_guid = ""
station_frequency = ""
station_market_city = ""
station_state = ""
station_display_name = ""
station_tag_line = ""
station_org_url = ""
station_description = ""
current_domain_name = ""
current_domain_path = ""
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True

#===============================================================================#
# Code
#===============================================================================#

# initialize exception helper
my_exception_helper = ExceptionHelper()

# configure database helper
db_host = "localhost"
db_port = 3306
db_username = "<username>"
db_password = "<password>"
db_database = "<database_name>"

# capture start datetime
start_dt = datetime.datetime.now()

# get instance of mysqldb helper
db_helper = MySQLdb_Helper( db_host, db_port, db_username, db_password, db_database )

# get connection (if you write to database, you need to commit with connection object).
db_connection = db_helper.get_connection()

# get cursor (opens connection if one not already open).
db_read_cursor = db_helper.get_cursor()

# make query SQL
sql_string = "SELECT DISTINCT place_name, admin_code1 FROM django_reference_data_postal_code ORDER BY admin_code1, place_name;"

# run the query.
db_read_cursor.execute( sql_string )
        
# get number of cities.
result_count = int( db_read_cursor.rowcount )

# loop.
domain_counter = 0
city_counter = 0
no_match_counter = 0
error_counter = 0
for i in range( result_count ):

    # increment city counter
    city_counter += 1
    
    # get row.
    current_row = db_read_cursor.fetchone()
    
    # retrieve values (default is to return rows as hashes of column name to value).
    current_city = current_row[ 'place_name' ]
    current_state = current_row[ 'admin_code1' ]
    
    # output the city
    print( "" )
    print( "=====================================================================" )
    print( "Retrieving NPR stations for " + current_city + ", " + current_state + " ( " + str( city_counter ) + " of " + str( result_count ) + " )" )
    
    # build URL for Station Finder API call
    npr_url = source_API_URL
    
    # add on city (first change spaces to "+")
    current_city_encoded = current_city.replace( " ", "+" )
    npr_url += "?city=" + current_city_encoded
    
    # add on state
    npr_url += "&state=" + current_state
    
    # store as source detail before we add on URL key.
    source_detail = npr_url
    
    # add on API key
    npr_url += "&apiKey=" + my_api_key
    
    print( "- Current URL: " + npr_url )

    # load the page.
    npr_xml = urllib2.urlopen( npr_url )

    # create beautifulsoup instance for API XML.  Uses lxml.
    #bs_parser = "html.parser"
    #bs_parser = "lxml"
    #bs_parser = "html5lib"
    npr_bs = BeautifulSoup( npr_xml, "xml" )
    
    if ( debug_flag == True ):
        print( str( npr_bs ) )
    #-- END DEBUG --#
    
    # look for message elements.
    message_list_bs = npr_bs.find_all( "message" )
    if ( ( message_list_bs ) and ( message_list_bs != None ) ):

        # loop over messages
        for current_message in message_list_bs:

            # get message details
            message_id = current_message[ "id" ]
            message_level = current_message[ "level" ]
            message_text = current_message.get_text()
            
            # print
            print( "- Status: id = " + message_id + "; level = " + message_level + "; text = " + message_text )
            
        #-- END loop over messages --#

    #-- END check to see if messages --#

    # get list of <station> elements
    station_list_bs = npr_bs.find_all( "station" )
    
    # loop over stations
    for current_station_bs in station_list_bs:
    
        # retrieve information on station.
        
        # try, for debugging and general programmatic politeness.
        try:

            # got an ID?
            if ( "id" in current_station_bs.attrs ):

                # got an ID?
                station_id = current_station_bs[ "id" ]
    
                # call letters
                temp_element = current_station_bs.find( "callLetters" )
                station_call_letters = temp_element.get_text()
                
                # band
                temp_element = current_station_bs.find( "band" )
                station_band = temp_element.get_text()
        
                # name (should be "<callLetters> <band>")
                temp_element = current_station_bs.find( "name" )
                station_name = temp_element.get_text()
        
                # GUID
                temp_element = current_station_bs.find( "guid" )
                station_guid = temp_element.get_text()
                
                # frequency
                temp_element = current_station_bs.find( "frequency" )
                station_frequency = temp_element.get_text()
        
                # market city
                temp_element = current_station_bs.find( "marketCity" )
                station_market_city = temp_element.get_text()
        
                # state
                temp_element = current_station_bs.find( "state" )
                station_state = temp_element.get_text()
        
                # display name
                temp_element = current_station_bs.find( "orgDisplayName" )
                station_display_name = temp_element.get_text()
        
                # tag line
                temp_element = current_station_bs.find( "tagline" )
                station_tag_line = temp_element.get_text()
        
                # organization URL (URL of type 1)
                temp_element = current_station_bs.find( "url", typeId = "1" )
                
                # got an element?
                if ( ( temp_element ) and ( temp_element != None ) ):
    
                    # yes.  Get URL string.
                    station_org_url = temp_element.get_text()
            
                    # got a URL?
                    if ( ( station_org_url ) and ( station_org_url != None ) and ( station_org_url != "" ) ):
                    
                        # make description include all information
                        station_description = station_call_letters + " " + station_band + ", " + station_frequency + " - " + station_market_city + ", " + station_state + " ( NPR ID: " + station_id + " )"
                        
                        print( "    - Found station: " + station_description )
            
                        # parse out domain and path
                        current_domain_name = django_reference_data.models.Reference_Domain.parse_URL( station_org_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
                        current_domain_path = django_reference_data.models.Reference_Domain.parse_URL( station_org_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )
                
                        print( "    - URL: \"" + current_domain_name + "\"; path: \"" + current_domain_path + "\"" )
            
                        # these are always the same
                        current_source = source
                        current_source_details = source_detail
                        current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
                        current_is_news = True
                
                        # update existing?
                        if ( do_update_existing == True ):
                
                            try:
                
                                # first, try looking up existing domain.
                                domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
                                domain_rs = domain_rs.filter( domain_name = current_domain_name )
                                domain_rs = domain_rs.filter( domain_path = current_domain_path )
                                current_domain_instance = domain_rs.get( description = station_description )
                            
                            except:
                            
                                # No matching row.  Create new instance.
                                current_domain_instance = django_reference_data.models.Reference_Domain()
                                
                                domain_counter += 1
                                
                            #-- END attempt to get existing row. --#
                
                        else:
                        
                            # not updating.  Just create new instance.
                            current_domain_instance = django_reference_data.models.Reference_Domain()
                        
                        #-- END check to see if we update existing. --#
                        
                        # set values
                        current_domain_instance.domain_name = current_domain_name
                        current_domain_instance.domain_path = current_domain_path
                        #current_domain_instance.long_name = None
                        current_domain_instance.description = station_description
                        current_domain_instance.source = current_source
                        current_domain_instance.source_details = current_source_details
                        current_domain_instance.domain_type = current_domain_type
                        current_domain_instance.is_news = current_is_news
                        #current_domain_instance.is_multimedia = False
                        #current_domain_instance.rank = current_rank
                        # current_domain_instance.address = station_address
                        current_domain_instance.state = station_state
                        #current_domain_instance.county = ""
                        current_domain_instance.city = station_market_city
                        #current_domain_instance.zip_code = nbc_zip_code
                        current_domain_instance.label = station_call_letters
                        current_domain_instance.external_id = station_id
                        current_domain_instance.guid = station_guid            
                
                        # save
                        current_domain_instance.save()
        
                    else:
                    
                        # no URL
                        print( "    - station " + station_name + " has no URL nested in its org URL element.  Moving on." )
                    
                    #-- END check to see if URL string present. --#
        
                else:
                
                    # no URL
                    print( "    - station " + station_name + " has no org URL element.  Moving on." )
                
                #-- END check to see if URL element present. --#
    
            else:
            
                # no ID
                print( "    - station element has no ID attribute, likely because our API query returned no results, and so returned a single empty station element, with no ID.  Moving on." )
                
                # no results
                no_match_counter += 1
            
                # output XML
                if ( debug_flag == True ):
                    print( npr_bs.prettify() )
                #-- END DEBUG --#
            
            #-- END check to see if URL element present. --#

        # Exception processing XML
        except Exception as e:
        
            # likely no ID attribute in empty station element, returned when
            #    query has no matches.  Print XML, error.
            print( "- Error - exception caught processing XML." )
            
            # increment error counter
            error_counter += 1
            
            # output Exception details.
            my_exception_helper.process_exception( e )
            
            # output XML
            print( npr_bs.prettify() )
        
        #-- END try/except around looking for station ID --#
    
    #-- END loop over stations --#

#-- END loop over cities from postal code table --#

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> Cities searched: " + str( city_counter ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> No Match: " + str( no_match_counter ) )
print( "==> Errors: " + str( error_counter ) )