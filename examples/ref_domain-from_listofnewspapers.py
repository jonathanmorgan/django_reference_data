# imports

# urllib
import datetime
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
#import python_utilities.beautiful_soup.beautiful_soup_helper

# django_reference_data
import django_reference_data.models

#===============================================================================#
# declare variables
#===============================================================================#

# declare variables - tracking performance
start_dt = None
end_dt = None
state_paper_counter = -1
city_counter = -1
domain_counter = -1
no_match_counter = -1
error_counter = -1
my_exception_helper = None

# processing state list.
state_list_url = ""
state_list_html = None
state_list_bs = None
state_li_list = None
state_li = None
state_url_dict = {}
state_name = ""
state_url = ""

# only process certain states
# skip 'Texas'.
#states_to_process_list = [ 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'American Samoa', 'Federated States of Micronesia', 'Guam', 'Northern Mariana Islands', 'Puerto Rico', 'US Virgin Islands' ]
states_to_process_list = []
do_update_existing = True
source = "listofnewspapers.com"
detail_string = ""

# processing a state's page.
state_html = None
state_bs = None
state_paper_list = None
state_paper_li = None
paper_name = ""
paper_url = ""
current_domain_instance = None
domain_rs = None

# fields we collect per domain.
bs_helper = None
current_domain_name = ""
slash_index = ""
current_domain_path = ""
current_description = ""
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True
current_rank = -1

#===============================================================================#
# Code
#===============================================================================#

# capture start datetime, initialize counters
start_dt = datetime.datetime.now()
state_paper_counter = 0
domain_counter = 0
no_match_counter = 0
error_counter = 0

# init beautiful soup helper
#bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# first, pull in list of state pages on this site.
state_list_url = "http://www.listofnewspapers.com/en/north-america/usa-newspapers-in-united-states-of-america.html"
state_list_html = urllib2.urlopen( state_list_url )

# create beautifulsoup instance for state list.
state_list_bs = BeautifulSoup( state_list_html, "html.parser" )

# get list of state URLs: <li class="linewspapers">
state_li_list = state_list_bs.find_all( "li", "linewspapers" )

# loop over states, opening up each's page and processing newspapers within.
for state_li in state_li_list:

    # get values
    state_name = state_li.get_text()
    state_url = state_li.a[ 'href' ]
    
    # process this state?
    if ( ( len( states_to_process_list ) == 0 ) or ( ( len( states_to_process_list ) > 0 ) and ( state_name in states_to_process_list ) ) ):

        # print next state:
        print( "----> Processed " + str( state_paper_counter ) + " papers." )
        print( "==> processing " + state_name + ": " + state_url )
        
        # load the state's URL
        state_html = urllib2.urlopen( state_url )
        
        # let BeautifulSoup parse it.
        state_bs = BeautifulSoup( state_html, "html.parser" )
        
        # get list of papers.
        state_paper_list = state_bs.find_all( "li", "linewspapers" )
        
        # loop over papers.
        state_paper_counter = 0
        for state_paper_li in state_paper_list:
        
            domain_counter += 1
            state_paper_counter += 1
        
            # get values
            paper_name = state_paper_li.get_text()
            paper_url = state_paper_li.a[ 'href' ]
        
            # collect information - init
            current_domain_name = ""
            slash_index = ""
            current_domain_path = ""
            current_description = ""
            current_source = ""
            current_source_details = ""
            current_domain_type = ""
            current_is_news = True
            current_rank = -1
            
            # description
            current_description = paper_name
            
            # parse out domain and path
            current_domain_name = django_reference_data.models.Reference_Domain.parse_URL( paper_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
            current_domain_path = django_reference_data.models.Reference_Domain.parse_URL( paper_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )
    
            # no rank
            
            # always the same for these.
            current_source = source
            current_source_details = state_url
            current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
            current_is_news = True
            
            detail_string = "====> Cleaned URL: " + paper_url + "; Domain: " + current_domain_name + "; path: " + current_domain_path + "; description: " + current_description

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

                        print( detail_string )
                        print( "--------> no match" )

                    #-- END check to see if domain found --#

                except:
                
                    # No matching row.  Create new instance.
                    current_domain_instance = django_reference_data.models.Reference_Domain()
                    no_match_counter += 1

                    print( detail_string )
                    print( "--------> no match (exception)" )
                    
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
            current_domain_instance.parse_and_store_URL( paper_url )
                        
            current_domain_instance.description = current_description
            current_domain_instance.source = current_source
            current_domain_instance.source_details = current_source_details
            current_domain_instance.domain_type = current_domain_type
            current_domain_instance.is_news = current_is_news
            #current_domain_instance.is_multimedia = False
            #current_domain_instance.rank = current_rank
            current_domain_instance.state = state_name
            #current_domain_instance.county = ""
            #current_domain_instance.city = ""
            #current_domain_instance.zip_code = ""
    
            # save
            current_domain_instance.save()

        #-- END loop over papers. --#

    else:
    
        # print next state:
        print( "==> skipping " + state_name + ": " + state_url )
    
    #-- END check to see if we proces this state. --#

#-- END loop over states in state list --#

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> No Match: " + str( no_match_counter ) )
print( "==> Errors: " + str( error_counter ) )