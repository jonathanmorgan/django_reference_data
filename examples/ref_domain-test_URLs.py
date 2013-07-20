# first, import reference domain class.
from django_reference_data.models import Reference_Domain

# if desired, set up result set of domains you want to test.

# in this case, we'll just test those that are not OK.
domain_rs = Reference_Domain.objects.filter( is_url_ok = False )

# output count, just for record-keeping.
print( domain_rs.count() ) # 638, for example

# invoke test method.
test_result = Reference_Domain.test_URLs( print_details_IN = True, domain_rs_IN = domain_rs )

# If you don't pass in a result set, it will just test all domains in table.