
# from foodOnline_main import settings
from vendor.models import Vendor
from django.conf import settings


#  it takes request and returen vendor dict
def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor = vendor)

# #  get Google API

def get_google_api(request):
    return {'TP_KEY' : settings.TP_KEY}
    # return {'GOOGlE_API_KEY' : settings.GOOGlE_API_KEY}