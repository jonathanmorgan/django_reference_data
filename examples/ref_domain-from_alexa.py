# imports

# urllib
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
#import python_utilities.beautiful_soup.beautiful_soup_helper

# django_reference_data
import django_reference_data.models

# declare variables
do_update_existing = True
url_prefix = ""
url_category_path = ""
page_index = -1
current_url = ""
domain_list_html = None
domain_list_bs = None
li_list = None
current_li = None
current_domain_instance = None
temp_bs = None

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

# init beautiful soup helper
#bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# loop over URLs
url_prefix = "http://www.alexa.com/topsites/category;"
page_index = -1
#url_category_path = "/Top/News" # all news
#page_count = 21
url_category_path = "/Top/News/Magazines_and_E-zines" # magazines and e-zines
page_count = 4
#url_category_path = "/Top/News/Newspapers" # all newspapers
#url_category_path = "/Top/News/Newspapers/Regional" # regional newspapers
for page_index in range( page_count ):

    # read in page of results from alexa.
    current_url = url_prefix + str( page_index ) + url_category_path
    domain_list_html = urllib2.urlopen( current_url )
    
    print( "==> Current URL: " + current_url )
    
    # initialize beautifulsoup instance
    domain_list_bs = BeautifulSoup( domain_list_html )
    
    # Looking for all <li> tags like this:
    # <li class="site-listing">
    li_list = domain_list_bs.find_all( "li", "site-listing" )
    
    # loop over <li> elements, creating reference_domain for each.
    for current_li in li_list:
    
        # collect information - init
        current_domain_name = ""
        slash_index = ""
        cleaned_url = ""
        current_domain_path = ""
        current_description = ""
        current_source = ""
        current_source_details = ""
        current_domain_type = ""
        current_is_news = True
        current_rank = -1
        
        # description
        temp_bs = current_li.find( "h2" )
        current_description = temp_bs.get_text()
        
        # domain name
        temp_bs = current_li.find( "span", "topsites-label" )
        cleaned_url = temp_bs.get_text()

        # parse out domain and path
        current_domain_name = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
        current_domain_path = django_reference_data.models.Reference_Domain.parse_URL( cleaned_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )

        # rank
        temp_bs = current_li.find( "div", "count" )
        current_rank = int( temp_bs.get_text() )
        
        # always the same for these.
        current_source = "alexa"
        current_source_details = current_url
        current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
        current_is_news = True
        
        # update existing?
        if ( do_update_existing == True ):

            try:

                # first, try looking up existing domain.
                domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
                domain_rs = domain_rs.filter( domain_name = current_domain_name )
                domain_rs = domain_rs.filter( domain_path = current_domain_path )
                current_domain_instance = domain_rs.get( description = current_description )
            
            except:
            
                # No matching row.  Create new instance.
                current_domain_instance = django_reference_data.models.Reference_Domain()
                
            #-- END attempt to get existing row. --#

        else:
        
            # not updating.  Just create new instance.
            current_domain_instance = django_reference_data.models.Reference_Domain()
        
        #-- END check to see if we update existing. --#
        
        # set values
        #current_domain_instance.domain_name = current_domain_name
        #current_domain_instance.domain_path = current_domain_path
        # current_domain_instance.long_name = None

        # parse and store the URL information.
        current_domain_instance.parse_and_store_URL( cleaned_url )
                        
        current_domain_instance.description = current_description
        current_domain_instance.source = current_source
        current_domain_instance.source_details = current_source_details
        current_domain_instance.domain_type = current_domain_type
        current_domain_instance.is_news = current_is_news
        # current_domain_instance.is_multimedia = False
        current_domain_instance.rank = current_rank

        # save
        current_domain_instance.save()
    
    #-- END loop over <li> elements --#

#-- END loop over pages in list. --#