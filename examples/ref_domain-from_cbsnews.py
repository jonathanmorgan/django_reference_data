# imports

# urllib
import datetime
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
import python_utilities.beautiful_soup.beautiful_soup_helper

# django_reference_data
import django_reference_data.models

#===============================================================================#
# declare variables
#===============================================================================#

# declare variables - tracking performance
start_dt = None
end_dt = None
domain_counter = -1
no_match_counter = -1
error_counter = -1
my_exception_helper = None

# constants-ish
do_update_existing = True
source = "cbsnews.com"
source_detail = "http://www.cbsnews.com/2100-18565_162-517034.html"
URL_FORWARD_STRING = "/forward/"

# processing state list.
station_list_url = ""
station_list_html = None
station_list_bs = None

# HTML navigation variables
state_name_list = []
div_storyText_list = None
div_storyText = None
state_bold_tag_list = None
state_counter = -1
state_name = ""
state_parent = None

# traversing siblings
current_sibling = None
is_sibling_text = False
current_sibling_element_name = ""
current_anchor_name = ""
is_next_state = False

# fields we collect per domain.
bs_helper = None
current_domain_name = ""
redirect_index = -1
slash_index = -1
current_domain_path = ""
current_description = ""
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True
current_rank = -1
station_name = ""
station_url = ""
cleaned_url = ""

#===============================================================================#
# Code
#===============================================================================#

# capture start datetime, initialize counters
start_dt = datetime.datetime.now()
domain_counter = 0
no_match_counter = 0
error_counter = 0

# init beautiful soup helper
bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# initialize state names we want to collect.
state_name_list = [ 'alabama', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusets', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'newmexico', 'newyork', 'northcarolina', 'northdakota', 'ohio', 'oklahoma', 'oregon', 'Pennsylvania', 'rhodeisland', 'southcarolina', 'southdakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'washingtondc', 'westvirginia', 'wisconsin', 'wyoming' ]

# first, pull in list of state pages on this site.
station_list_url = "http://www.cbsnews.com/2100-18565_162-517034.html"
station_list_html = urllib2.urlopen( station_list_url )

# create beautifulsoup instance for state list.
#bs_parser = "html.parser"
#bs_parser = "lxml"
bs_parser = "html5lib"
station_list_bs = BeautifulSoup( station_list_html, bs_parser )

# get storytext div:  <div class="storyText">
div_storyText_list = station_list_bs.find_all( "div", "storyText" )
div_storyText = div_storyText_list[ 0 ]

# get all bold tags
state_bold_tag_list = div_storyText.find_all( "b" )

# initialize variables
state_counter = 0

# loop over bold tags
for state_bold_tag in state_bold_tag_list:

    # increment counter
    state_counter += 1

    # get state text
    state_name = state_bold_tag.get_text()

    # skip the first 2
    if ( state_counter > 2 ):

        print( "Processing " + state_name )
        
        # initialize variables
        is_next_state = False
        current_anchor_name = ""
        
        # strip colon off end of name.
        state_name = state_name.replace( ":", "" )
        
        # get parent of state
        state_parent = state_bold_tag.parent

        # get next sibling
        current_sibling = state_parent.next_sibling
        current_sibling_element_name = bs_helper.bs_get_element_name( current_sibling )

        # loop over next siblings until we get to another <b>
        while ( ( current_sibling ) and ( is_next_state == False ) ):
        
            # initialize variables
            current_anchor_name = ""
        
            # is this an <a> tag?
            if ( current_sibling_element_name == "a" ):
            
                # does it have a name attribute?
                if ( "name" in current_sibling.attrs ):

                    # name attribute found.  This is the next state.
                    is_next_state = True                    

                else:
                
                    # no name attribute.  This is a new station link.
                    print( "- Found station: " + current_sibling.get_text() )
                    domain_counter += 1
                    
                    # get values
                    station_name = current_sibling.get_text()
                    station_url = current_sibling[ 'href' ]
                
                    # collect information - init
                    current_domain_name = ""
                    slash_index = ""
                    current_domain_path = ""
                    current_description = ""
                    current_city = ""
                    current_source = ""
                    current_source_details = ""
                    current_domain_type = ""
                    current_is_news = True
                    current_rank = -1
                    
                    # description
                    current_description = station_name
                    
                    # split description into an array on spaces.
                    station_name_list = station_name.split()
                    
                    # remove the last item
                    station_name_list.pop()
                    
                    # convert back to string.
                    current_city = " ".join( station_name_list )
                    
                    # domain name
                    cleaned_url = station_url
                    
                    # first, see if this URL contains "/forward/"
                    redirect_index = cleaned_url.find( URL_FORWARD_STRING )
                    if ( redirect_index >= 0 ):
                    
                        # yes.  strip off everything before "/forward/"
                        cleaned_url = cleaned_url[ ( redirect_index + len( URL_FORWARD_STRING ) ) : ]
                    
                    #-- END check to see if domain has "/forward/" --#

                    # parse out domain and path
                    current_domain_name = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
                    current_domain_path = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )
            
                    # no rank
                    
                    # always the same for these.
                    current_source = source
                    current_source_details = source_detail
                    current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
                    current_is_news = True
                    
                    print( "    - Cleaned URL: " + cleaned_url + "; Domain: " + current_domain_name + "; path: " + current_domain_path )
                    
                    # get Reference_Domain instance
                    
                    # update existing?
                    if ( do_update_existing == True ):
        
                        try:
            
                            # first, try looking up existing domain.
                            #domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
                            #domain_rs = domain_rs.filter( domain_name = current_domain_name )
                            #domain_rs = domain_rs.filter( domain_path = current_domain_path )
                            #current_domain_instance = domain_rs.get( description = current_description )
                        
                            # use lookup_record() method.  Returns None if
                            #    not found.
                            current_domain_instance = django_reference_data.models.Reference_Domain.lookup_record( source_IN = current_source, domain_name_IN = current_domain_name, domain_path_IN = current_domain_path, description_IN = current_description )
                            
                            # got anything?
                            if ( current_domain_instance == None ):
                            
                                # nothing returned.  Create new instance.
                                current_domain_instance = django_reference_data.models.Reference_Domain()
                                no_match_counter += 1
                            
                            #-- END check to see if domain found --#

                        except:
                        
                            # No matching row.  Create new instance.
                            current_domain_instance = django_reference_data.models.Reference_Domain()
                            no_match_counter += 1
                            
                        #-- END attempt to get existing row. --#
        
                    else:
                    
                        # not updating.  Just create new instance.
                        current_domain_instance = django_reference_data.models.Reference_Domain()
                    
                    #-- END check to see if we update existing. --#
                    
                    # set values
                    #current_domain_instance.domain_name = current_domain_name
                    #current_domain_instance.domain_path = current_domain_path
                    #current_domain_instance.long_name = None

                    # parse and store the URL information.
                    current_domain_instance.parse_and_store_URL( cleaned_url )
                        
                    current_domain_instance.description = current_description
                    current_domain_instance.source = current_source
                    current_domain_instance.source_details = current_source_details
                    current_domain_instance.domain_type = current_domain_type
                    current_domain_instance.is_news = current_is_news
                    #current_domain_instance.is_multimedia = False
                    #current_domain_instance.rank = current_rank
                    current_domain_instance.state = state_name
                    #current_domain_instance.county = ""
                    current_domain_instance.city = current_city
                    #current_domain_instance.zip_code = ""
            
                    # save
                    current_domain_instance.save()                    
                
                #-- END check to see if current anchor has a name --#
            
            #-- END check to see if anchor tag. --#
            
            # get next sibling and next sibling's element name.
            current_sibling = current_sibling.next_sibling
            current_sibling_element_name = bs_helper.bs_get_element_name( current_sibling )
            
        #-- END loop over siblings --#

    else:
    
        print( "==> Skipping " + state_name )
        
    #-- END

#-- END loop over state bold tags. --#

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> No Match: " + str( no_match_counter ) )
print( "==> Errors: " + str( error_counter ) )