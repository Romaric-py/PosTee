from controllers.controller import *
from controllers.auth_controller import *

routes = {
    'GET': {
        '/': home,
        '/about': about,
        '/login': login_get,
        '/register': register_get,
        '/feed': feed,
    },
    'POST': {
        '/login': login_post,
        '/register': register_post,
    }
}