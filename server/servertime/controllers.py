from datetime import datetime
from protocol import make_200

def timestamp_controller(request):
    return make_200(request, datetime.now().timestamp())
