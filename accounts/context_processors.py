
from vendor.models import Vendor


#  it takes request and returen vendor dict
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor = vendor)