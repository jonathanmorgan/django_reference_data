# Stations were collected from http://www.nbc.com/local-stations/ manually,
#    Placed in a text file that was then added to a spreadsheet.  Used Excel
#    macros to split address into fields, then used Navicat to import the table
#    as a database table.  Now to loop, add domains to reference_domains.

# imports
import datetime
import gc
import django.db
import django_reference_data.models
from python_utilities.database.MySQLdb_helper import MySQLdb_Helper

# constants-ish
do_update_existing = True
source = "nbc.com"
source_detail = "http://www.nbc.com/local-stations/"

#===============================================================================#
# declare variables
#===============================================================================#

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

# values from the NBC table
nbc_call_sign = ""
nbc_full_address = ""
nbc_address = ""
nbc_city = ""
nbc_state = ""
nbc_zip_code = ""
nbc_url = ""
nbc_description = ""
current_domain_name = ""
current_domain_path = ""
current_source = ""
current_source_details = ""
current_domain_type = ""
current_is_news = True

# tracking performance
start_dt = None
end_dt = None
domain_counter = -1
no_match_counter = -1
error_counter = -1

#===============================================================================#
# Code
#===============================================================================#

# capture start datetime, initialize counters
start_dt = datetime.datetime.now()
domain_counter = 0
no_match_counter = 0
error_counter = 0

# configure database helper
db_host = "localhost"
db_port = 3306
db_username = "<username>"
db_password = "<password>"
db_database = "<database_name>"

# get instance of mysqldb helper
db_helper = MySQLdb_Helper( db_host, db_port, db_username, db_password, db_database )

# get connection (if you write to database, you need to commit with connection object).
db_connection = db_helper.get_connection()

# get cursor (opens connection if one not already open).
db_read_cursor = db_helper.get_cursor()

# make query SQL
sql_string = "SELECT * FROM django_reference_data_nbc_stations ORDER BY call_sign ASC;"

# run the query.
db_read_cursor.execute( sql_string )
        
# get number of domains.
result_count = int( db_read_cursor.rowcount )

# loop.
domain_counter = 0
for i in range( result_count ):

    # increment counter
    domain_counter += 1

    # get row.
    current_row = db_read_cursor.fetchone()
    
    # get values (default is to return rows as hashes of column name to value).
    nbc_call_sign = current_row[ 'call_sign' ]
    nbc_full_address = current_row[ 'full_address' ]
    nbc_address = current_row[ 'address' ]
    nbc_city = current_row[ 'city' ]
    nbc_state = current_row[ 'state' ]
    nbc_zip_code = current_row[ 'zip_code' ]
    nbc_url = current_row[ 'url' ]
    
    # got a URL?  If not, nothing we can do.
    if ( ( nbc_url ) and ( nbc_url != "" ) ):
    
        # make description include all information
        nbc_description = nbc_call_sign + " - " + nbc_full_address + " - " + nbc_url
        
        # parse out domain and path
        current_domain_name = django_reference_data.models.Reference_Domain.parse_URL( nbc_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_DOMAIN )
        current_domain_path = django_reference_data.models.Reference_Domain.parse_URL( nbc_url, django_reference_data.models.Reference_Domain.URL_PARSE_RETURN_PATH )

        # these are always the same
        current_source = source
        current_source_details = source_detail
        current_domain_type = django_reference_data.models.Reference_Domain.DOMAIN_TYPE_NEWS
        current_is_news = True

        print( "==> Cleaned URL: " + nbc_url + "; Domain: " + current_domain_name + "; path: " + current_domain_path + "; description: " + nbc_description )

        # update existing?
        if ( do_update_existing == True ):

            try:

                # first, try looking up existing domain.
                #domain_rs = django_reference_data.models.Reference_Domain.objects.filter( source = current_source )
                #domain_rs = domain_rs.filter( domain_name = current_domain_name )
                #domain_rs = domain_rs.filter( domain_path = current_domain_path )
                #current_domain_instance = domain_rs.get( description = current_description )
            
                # use lookup_record() method.  Returns None if not found.
                current_domain_instance = django_reference_data.models.Reference_Domain.lookup_record( source_IN = current_source, domain_name_IN = current_domain_name, domain_path_IN = current_domain_path, description_IN = nbc_description )
                
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
        current_domain_instance.parse_and_store_URL( nbc_url )
        
        current_domain_instance.description = nbc_description
        current_domain_instance.source = current_source
        current_domain_instance.source_details = current_source_details
        current_domain_instance.domain_type = current_domain_type
        current_domain_instance.is_news = current_is_news
        #current_domain_instance.is_multimedia = False
        #current_domain_instance.rank = current_rank
        current_domain_instance.address = nbc_address
        current_domain_instance.state = nbc_state
        #current_domain_instance.county = ""
        current_domain_instance.city = nbc_city
        current_domain_instance.zip_code = nbc_zip_code

        # save
        current_domain_instance.save()                    

    #-- END check to see if there is a URL. --#
        
    # clear caches, performance stuff, etc.  Try garbage
    #    collecting, not clearing django cache, to start.
    gc.collect()
    django.db.reset_queries()

#-- END loop over domains. --#

# close the cursor and connection.
db_helper.close()

# a little overview
end_dt = datetime.datetime.now()
print( "==> Started at " + str( start_dt ) )
print( "==> Finished at " + str( end_dt ) )
print( "==> Duration: " + str( end_dt - start_dt ) )
print( "==> Domains: " + str( domain_counter ) )
print( "==> No Match: " + str( no_match_counter ) )
print( "==> Errors: " + str( error_counter ) )