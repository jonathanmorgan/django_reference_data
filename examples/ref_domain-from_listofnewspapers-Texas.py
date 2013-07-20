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
domain_counter = -1
no_match_counter = -1
error_counter = -1
my_exception_helper = None

# declare variables
do_update_existing = True

# processing state list.
state_name = ""
state_url = ""
state_file_path = ""
state_file = None

# processing a state's page.
state_html = None
state_bs = None
state_paper_list = None
state_paper_li = None
paper_name = ""
paper_url = ""
current_domain_instance = None
paper_counter = -1

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
domain_counter = 0
no_match_counter = 0
error_counter = 0

# init beautiful soup helper
#bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# clean out broken texas domain rows.
'''
DELETE from `django_reference_data_reference_domain`
WHERE source_details LIKE '%in-texas%';
'''

state_name = "Texas"
state_url = "http://www.listofnewspapers.com/en/north-america/texan-newspapers-in-texas.html"
state_file_path = "texan-newspapers-in-texas-TIDY.html"

# print next state:
print( "==> processing " + state_name + ": " + state_file_path )

# load the state's HTML
state_file = open( state_file_path, "r" )
state_html = state_file.read()

# let BeautifulSoup parse it.
state_bs = BeautifulSoup( state_html, "html.parser" )

# get list of papers.
state_paper_list = state_bs.find_all( "li", "linewspapers" )

print( "- paper count: " + str( len( state_paper_list ) ) )

# loop over papers.
paper_counter = 0
for state_paper_li in state_paper_list:

    paper_counter += 1
    domain_counter += 1

    print( "- paper " + str( paper_counter ) + ": " + str( state_paper_li ) )

    # get values
    paper_name = state_paper_li.get_text()
    paper_url = state_paper_li.a[ 'href' ]
    
    print( "    - " + paper_name + ": " + paper_url )

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
    current_source = "listofnewspapers.com"
    current_source_details = state_url
    current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
    current_is_news = True
    
    # get Reference_Domain instance

    # update existing?
    if ( do_update_existing == True ):

        try:

            # first, try looking up existing domain.
            #domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
            #domain_rs = domain_rs.filter( domain_name = current_domain_name )
            #current_domain_instance = domain_rs.get( domain_path = current_domain_path )
        
            # use lookup_record() method.  Returns None if
            #    not found.
            current_domain_instance = django_reference_data.models.Reference_Domain.lookup_record( source_IN = current_source, domain_name_IN = current_domain_name, domain_path_IN = current_domain_path )
            
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

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> No Match: " + str( no_match_counter ) )
print( "==> Errors: " + str( error_counter ) )