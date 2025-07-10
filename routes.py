from controller import *

routes = {
    'GET': {
        '/': root,
        '/home': home,
        '/users': get_users,
        '/about': about,
    },
    'POST': {
        
    }
}