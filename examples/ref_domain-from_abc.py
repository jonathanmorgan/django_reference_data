'''
Will need to do some manual cleanup after you run this script.  Couldn't write
   it so it dealt with all the inconsistencies in the HTML.  In particular, look
   for places where address area is non-standard (multiple telephone numbers,
   etc.).  URL/domain/path collection doesn't seem to be affected.
'''

# imports

# urllib
import urllib2

# beautifulsoup 4
from bs4 import BeautifulSoup

# python_utilties
import python_utilities.beautiful_soup.beautiful_soup_helper

# django_reference_data
import django_reference_data.models

# constants-ish
COMMENT_STATE_CONTAINS = "STATE"
COMMENT_STATION_CONTAINS = "STATION INFORMATION ROW"
URL_FORWARD_STRING = "goto="

# declare variables
do_update_existing = True
bs_helper = None
page_list = []
page_counter = -1
page_url = ""
page_html = ""
page_bs = None
page_table_list_bs = None
station_table_bs = None
tbody_list_bs = None
tbody_bs = None
tbody_children_bs = None
child_counter = -1
current_child = None
current_state = ""
last_state = ""
is_comment = ""
current_text = ""
temp_text = ""

# declare variables - grabbing station data.
station_city = ""
station_call_sign = ""
station_address = ""
station_state = ""
station_zip_code = ""
station_phone = ""
station_email = ""
station_url = ""
station_description = ""
cleaned_url = ""
station_domain_name = ""
station_domain_path = ""

# declare variables - navigating station HTML.
station_tr_bs = None
station_tr_children_bs = None
station_td_counter = -1
station_td_list = None
current_td = None
station_td_align = ""
br_list_bs = None
current_br_bs = None
br_counter = -1
a_list_bs = None
current_a_bs = None
a_counter = -1

# declare variables - dealing with call sign, address, and phone
outer_font_bs = None
inner_font_list = None
inner_font_counter = -1
current_font_bs = None
bold_list_bs = None
current_bold_bs = None
bold_bs = None
font_br_list_bs = None
font_br_counter = -1
address_item_list = []
is_text = False
current_text = ""
font_child_list_bs = None
font_child_bs = None
address_item_count = -1
city_state_zip_string = ""
city_index = -1
city_state_zip_item_list = []

# declare variables - dealing with web address, email address.
anchor_list_bs = None
current_anchor_bs = None
href_value = ""

# declare variables - meta-data for each station
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True
source = "http://site.abc.go.com/site/localstations.html"

# declare variables - store in database.
current_domain_instance = None

# make instance of BeautifulSoupHelper
bs_helper = python_utilities.beautiful_soup.beautiful_soup_helper.BeautifulSoupHelper()

# create list of pages we need to parse.
page_list.append( "http://site.abc.go.com/site/al_ak.html" )
page_list.append( "http://site.abc.go.com/site/az_ar.html" )
page_list.append( "http://site.abc.go.com/site/ca.html" )
page_list.append( "http://site.abc.go.com/site/co_ct_de_dc.html" )
page_list.append( "http://site.abc.go.com/site/fl.html" )
page_list.append( "http://site.abc.go.com/site/g_b_vi_pr.html" )
page_list.append( "http://site.abc.go.com/site/ga.html" )
page_list.append( "http://site.abc.go.com/site/hi_id.html" )
page_list.append( "http://site.abc.go.com/site/il.html" )
page_list.append( "http://site.abc.go.com/site/in_ia.html" )
page_list.append( "http://site.abc.go.com/site/ks_ky_la.html" )
page_list.append( "http://site.abc.go.com/site/me_md_ma.html" )
page_list.append( "http://site.abc.go.com/site/mi.html" )
page_list.append( "http://site.abc.go.com/site/mn_ms.html" )
page_list.append( "http://site.abc.go.com/site/mo_mt.html" )
page_list.append( "http://site.abc.go.com/site/nc_nd.html" )
page_list.append( "http://site.abc.go.com/site/ne_nv_nh_nj_nm.html" )
page_list.append( "http://site.abc.go.com/site/ny.html" )
page_list.append( "http://site.abc.go.com/site/oh_ok.html" )
page_list.append( "http://site.abc.go.com/site/or_pa.html" )
page_list.append( "http://site.abc.go.com/site/ri_sc_sd.html" )
page_list.append( "http://site.abc.go.com/site/tn.html" )
page_list.append( "http://site.abc.go.com/site/tx.html" )
page_list.append( "http://site.abc.go.com/site/ut_vt_va_wa.html" )
page_list.append( "http://site.abc.go.com/site/wv_wi_wy.html" )

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

    # get all tables in page
    #page_table_list_bs = page_bs.find_all( "table" )
    
    # third table contains state-by-state list of stations.
    #station_table_bs = page_table_list_bs[ 2 ]
    
    # first, need to get <tbody> element
    #tbody_bs = station_table_bs.find( "tbody" )
    
    # first, need to get <tbody> elements
    tbody_list_bs = page_bs.find_all( "tbody" )
    
    # third <tbody> contains state-by-state list of stations.
    tbody_bs = tbody_list_bs[ 2 ]
    
    # walk table.
    tbody_children_bs = tbody_bs.children
    
    # loop over children
    child_counter = 0
    current_state = ""
    last_state = ""
    for current_child in tbody_children_bs:
    
        # increment counter.
        child_counter += 1
        
        # find our way through the file based on comments:
        # <!-- STATE... --> = start of a new state.
        # <!-- STATION INFORMATION ROW --> = station <tr>
        
        # first, check to see if comment
        is_comment = bs_helper.bs_is_comment( current_child )
        if ( is_comment == True ):
        
            # is a comment.  Check to see if it is one we care about.
            if ( COMMENT_STATE_CONTAINS in current_child ):
            
                # state marker.
                print( "========== found state marker comment ( child " + str( child_counter ) + " ): " + str( current_child ) )
                
            elif ( COMMENT_STATION_CONTAINS in current_child ):
            
                # not a comment - move on.
                print( "========== found station marker comment ( child " + str( child_counter ) + " ): " + str( current_child ) )
                
                # now, we walk its children.
                
                # loop until NOT NavigableString.
                station_tr_bs = current_child.next_sibling
                while( bs_helper.bs_is_navigable_text( station_tr_bs ) == True ):
                
                    # get next sibling.
                    station_tr_bs = station_tr_bs.next_sibling
                
                #-- END loop to get past any white space --#
                
                # for Delaware, check if this is a comment, and if so, if it is a
                #    state comment.  If there is a state comment immediately
                #    following a station comment, that means there are no
                #    stations for that state.  Move on.
                if ( ( bs_helper.bs_is_comment( station_tr_bs ) == False ) and ( COMMENT_STATE_CONTAINS not in current_child ) ):
                                
                    # get children, initialize variables.
                    station_tr_children_bs = station_tr_bs.children
                    station_td_list = station_tr_bs.find_all( "td" )
                    station_td_align = ""
                    station_td_counter = 0
                    station_city = ""
                    station_call_sign = ""
                    station_address = ""
                    station_state = ""
                    station_zip_code = ""
                    station_phone = ""
                    station_email = ""
                    station_url = ""
                    
                    # Could also find <td>s, not go over children.  If go over
                    #    children, skip text, only look at elements with name = "td".
                    #    If not children, just make sure that "find_all" preserves
                    #    order, else you'll have to make the detection based on
                    #    contents instead of the position in the list of children.
                    
                    #for current_td in station_tr_children_bs:
                    for current_td in station_td_list:
                    
                        # is NOT text, and is name = "td"?
                        is_text = bs_helper.bs_is_navigable_text( current_td )
                        if ( ( is_text == False ) and ( current_td.name.lower() == "td" ) ):
                    
                            # increment counter
                            station_td_counter += 1
                            
                            # only care about numbers:
                            # - 1 - city name: <td> has align attribute that = "right"
                            # try/except, since it throws an exception if
                            #    attribute not present in element.
                            try:
                            
                                station_td_align = current_td[ "align" ]
                                
                            except:
                            
                                station_td_align = None
                                
                            #-- END check to see if <td> has an "align" attribute. --#

                            # - 3 - call sign, address, telephone: contains <br />
                            br_list_bs = current_td.find_all( "br" )
                            br_counter = 0
                            for current_br_bs in br_list_bs:

                                # increment counter
                                br_counter += 1
                            
                            #-- END loop over <br> elements --#

                            # - 5 - URL and/or email: contains <a> (email href attribute contains "mailto").
                            a_list_bs = current_td.find_all( "a" )
                            a_counter = 0
                            for current_a_bs in a_list_bs:

                                # increment counter
                                a_counter += 1
                            
                            #-- END loop over <a> elements --#

                            #if ( station_td_counter == 1 ):
                            # now, check for ALIGN="RIGHT"
                            if ( ( station_td_align ) and ( station_td_align != None ) and ( station_td_align != "" ) and ( station_td_align.lower() == "right" ) ):
                            
                                # city name - get text.
                                station_city = current_td.get_text().strip()
                            
                            #elif ( station_td_counter == 3 ):
                            # check for presence of <br> tags.                            
                            elif ( br_counter > 0 ):
                            
                                # call sign, address, phone.
                                
                                # more walking.  first, get first child - should be a
                                #    single <font> tag.
                                outer_font_bs = current_td.find( "font" )
                                
                                # then, in that element, get all the "font" tags.
                                inner_font_list = outer_font_bs.children
                                
                                # loop
                                inner_font_counter = 0
                                for current_font_bs in inner_font_list:
    
                                    # is text?
                                    is_text = bs_helper.bs_is_navigable_text( current_font_bs )
                                    if ( ( is_text == False ) and ( current_font_bs.name.lower() == "font" ) ):
    
                                        # increment counter
                                        inner_font_counter += 1
            
                                        # look for bold tag.  If not found, returns None.
                                        bold_bs = None
                                        bold_list_bs = current_font_bs.find_all( "b" )
                                        for current_bold_bs in bold_list_bs:
                                        
                                            # get text.
                                            temp_text = current_bold_bs.get_text()
                                            
                                            # is it "broadcasts in HDTV"?
                                            if ( temp_text.lower() != "broadcasts in hdtv" ):
                                                
                                                # not "broadcast in HDTV" - use this one.
                                                bold_bs = current_bold_bs
                                                
                                            #-- END check to see if "broadcast in HDTV --#
                                            
                                        #-- END loop over bold tags. --#
                                        
                                        # print( "*** bold_bs = " + str( bold_bs ) )
                                        
                                        # also look for <br> tags.
                                        font_br_list_bs = current_font_bs.find_all( "br" )
                                        font_br_counter = 0
                                        for current_br_bs in font_br_list_bs:
            
                                            # increment counter
                                            font_br_counter += 1
                                        
                                        #-- END loop over <br> elements --#
                                        
                                        if ( ( bold_bs ) and ( bold_bs != None ) and ( font_br_counter == 0 ) ):
                                        
                                            # found a <b> - this is the call sign <font> tag.
                                            station_call_sign = bold_bs.get_text()
                                            
                                        else:
                                        
                                            # no <b>.  This is the address/phone <font> tag.
                                            address_item_list = []
                                            
                                            # one last child walk.
                                            font_child_list_bs = current_font_bs.children
                                            for font_child_bs in font_child_list_bs:
                                            
                                                # is this text?
                                                is_text = bs_helper.bs_is_navigable_text( font_child_bs )
                                                if ( is_text == True ):
                                                
                                                    # it is text.  Add it to our list.
                                                    address_item_list.append( font_child_bs )
                                                
                                                #-- END check to see if text --#
                                            
                                            #-- END loop over children of font tag. --#
                                            
                                            print( "Address item list: " + str( address_item_list ) )
                                            
                                            # last item will always be phone number.
                                            station_phone = str( address_item_list.pop() )
                                            
                                            # now, parse out items in address list.  Start by
                                            #    getting count of items.
                                            address_item_count = len( address_item_list )
                                            
                                            # was count 1, 2 or other (some addresses are all in one).
                                            if ( address_item_count == 1 ):
            
                                                # originally were only two items.  This means
                                                #    address and city state zip all on one
                                                #    line.  Find city, place everything
                                                #    before in address, everything after gets
                                                #    parsed as city state zip.
            
                                                # get remaining string.
                                                temp_text = address_item_list.pop()
                                                
                                                # got a city?
                                                if ( ( station_city ) and ( station_city != None ) and ( station_city != "" ) ):
                                                
                                                    # yes.  Is it located in the remaining string?
                                                    city_index = temp_text.find( station_city )
                                                    if ( city_index > -1 ):
                                                    
                                                        # take text up to city as address,
                                                        #    after it as city_state_zip.
                                                        station_address = temp_text[ : city_index ]
                                                        city_state_zip_string = temp_text[ city_index : ]
                                                    
                                                    else:
                                                    
                                                        # error.  Just use the temp_text as
                                                        #    both address and city_state_zip.
                                                        station_address = temp_text
                                                        city_state_zip_string = temp_text
                                                    
                                                    #-- END check to see if city is in address text --#
                                                
                                                #-- END check to see if we have a city --#
                                            
                                            elif ( address_item_count == 2 ):
            
                                                # this is easier.  item 1 is address, item 2
                                                #    is <city>, <state> <zip>
                                                city_state_zip_string = address_item_list.pop()
                                                station_address = address_item_list.pop()
                                                
                                            else:
                                            
                                                # not 1 or 2 items - either 0 or more...
                                                # broken.  put string contents of remaining
                                                #    list items in both station_address and
                                                #    city_state_zip_string.
                                                temp_text = ";".join( address_item_list )
                                                station_address = temp_text
                                                city_state_zip_string = temp_text
                                                
                                            #-- END check to see how many address items we have left. --#
                                            
                                            # see if we have a city_state_zip_string.
                                            if ( ( city_state_zip_string ) and ( city_state_zip_string != "" ) ):
                                            
                                                # we do.  Assume format of <city>, <state> <zip>
                                                
                                                # first, split on white space.
                                                city_state_zip_item_list = city_state_zip_string.split()
                                                
                                                # last item should be zip code.
                                                station_zip_code = city_state_zip_item_list.pop().strip()
                                                
                                                # then, put string back together
                                                temp_text = " ".join( city_state_zip_item_list )
                                                
                                                # now, split on comma.
                                                city_state_zip_item_list = temp_text.split( " " )
                                            
                                                # last item should be state.
                                                station_state = city_state_zip_item_list.pop().strip().upper()
                                            
                                            #-- END check to see if city_state_zip_string. --#
                                        
                                        #-- END check for <b> tag. --#
    
                                    #-- END check to see if this is a <font> tag, not text (or something else) --#
                                    
                                #-- END loop over inner <font> tags --#
                            
                            #elif ( station_td_counter == 5 ):
                            # finally, check for <a> tags.
                            elif ( a_counter > 0 ):
                            
                                # this is the <td> that will contain links to web site,
                                #    email address, if they are present.
                                
                                # first, get list of all anchor tags in this element.
                                anchor_list_bs = current_td.find_all( "a" )
        
                                # loop
                                for current_anchor_bs in anchor_list_bs:
                                
                                    # get href attribute value.
                                    href_value = current_anchor_bs[ 'href' ]
                                    
                                    # does it contain "mailto"?
                                    if ( "mailto" in href_value ):
                                    
                                        # it does.  This is email address.
                                        station_email = href_value
                                        
                                    else:
                                    
                                        # no - this is web site.
                                        station_url = href_value
                                    
                                    #-- END check to see if mailto --#
                                
                                #-- END loop over anchor list. --#
                            
                            #-- END check to see if it is a <td> we care about. --#
    
                        #-- END check to see if current item is <td>, not text (or something else). --#
                        
                    #-- END loop over children to get station info. --#
                    
                    # make station description
                    station_description = station_call_sign + " - " + station_address + "; " + station_city + ", " + station_state + " " + station_zip_code
                    
                    # do we have a URL?
                    if ( ( station_url ) and ( station_url != None ) and ( station_url != "" ) ):
                    
                        # adding to database.
                        print( "    ===> adding station: " + station_description )
    
                        # domain name
                        cleaned_url = station_url
                        
                        # first, see if this URL contains "goto="
                        redirect_index = cleaned_url.find( URL_FORWARD_STRING )
                        if ( redirect_index >= 0 ):
                        
                            # yes.  strip off everything before "goto="
                            cleaned_url = cleaned_url[ ( redirect_index + len( URL_FORWARD_STRING ) ) : ]
                        
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
                        current_domain_instance.domain_name = station_domain_name
                        current_domain_instance.domain_path = station_domain_path
                        #current_domain_instance.long_name = None
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
                        current_domain_instance.email = station_email
                        current_domain_instance.label = station_call_sign
                
                        # save
                        current_domain_instance.save()                    
                    
                        print( "    - Added: " + str( current_domain_instance ) )
                
                    else:
                    
                        # no URL - not adding to database.
                        print( "    ===> no URL: " + station_description )
    
                    #-- END check to see if station_url.
                    
                #-- END check to see if station comment is immediately followed by STATE comment (if so, Delaware, which is serviced by Pennsylvania and Maryland). --#

            else:
            
                # not a comment we care about - move on.
                print( "========== ignoring comment ( child " + str( child_counter ) + " ): " + str( current_child ) )
            
            #-- END check to see if we care about comment --#            
        
        else:
        
            # not a comment - move on.
            if ( bs_helper.bs_is_navigable_text( current_child ) == True ):
            
                # text.  output that we are ignoring it.
                print( "========== ignoring child " + str( child_counter ) + " - text" )
            
            else:
            
                # element - output that we are ignoring it.
                print( "========== ignoring child " + str( child_counter ) + " - element = " + current_child.name )
                
            #-- END check to see if text. --#
            
        #-- END check to see if comment. --#
    
    #-- END loop over elements in table ---#

#-- END loop over pages in page list. --#