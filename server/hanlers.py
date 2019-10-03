import json
import logging
from protocol import validate_request, make_404, make_500
from middlewares import compression_middleware

@compression_middleware
def handle_tcp_request(bytes_request, action_mapping):
    request = json.loads(bytes_request)
    if validate_request(request):
        action = request.get('action')
        controller = action_mapping.get(action)

        if controller:
            try:
                response = controller(request)
                logging.debug(f'Request: {bytes_request.decode()}')
            except Exception as err:
                response = make_500(request)
                logging.critical(err)
        else:
            response = make_404(request)
            logging.error(f'Action with name {action} not found')
    else:
        response = make_404(request, 'Request is not valid')
        logging.error(f'Wrong Request: {request}')

    string_response = json.dumps(response)
    return string_response.encode()
