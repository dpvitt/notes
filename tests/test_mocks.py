
register_valid_user = {
    'email': 'wiley@example.com',
    'username': 'wiley',
    'password': 'cat',
    'password2': 'cat'
}

register_invalid_user = {
    'email': 'skepta@example.com',
    'username': 'skepta',
    'password': 'cat',
    'password2': 'dog'
}

login_valid_user = {
    'username': 'wiley',
    'password': 'cat'
}

login_invalid_user = {
    'username': 'skepta',
    'password': 'cat'
}

login_empty_user = {
    'username': '',
    'password': 'frog'
}

note_body = {
    'body': 'this is an example note',
    'tag': 'test tag'
}

note_updated_body = {
    'body': 'this is an updated note'
}

note_empty = {
    'body': ''
}
