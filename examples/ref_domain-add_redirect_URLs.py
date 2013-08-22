# first, import reference domain class.
from django_reference_data.models import Reference_Domain

# if desired, set up result set of domains you want to process.

# for example, could just process those that are OK.
# domain_rs = Reference_Domain.objects.filter( is_url_ok = True )

# output count, just for record-keeping.
# print( domain_rs.count() ) # 8834, for example.

# invoke test method.
# test_result = Reference_Domain.make_rows_for_redirect_URLs( print_details_IN = True, domain_rs_IN = domain_rs )

# If you don't pass in a result set, it will just test all domains in table that
#    have a redirect.
test_result = Reference_Domain.make_rows_for_redirect_URLs( print_details_IN = True )