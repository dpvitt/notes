
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
    'tag': '1'
}

note_body_2 = {
    'body': 'another note',
    'tag': '2'
}

note_body_public = {
    'body': 'this is an example note',
    'tag': '1',
    'public': 'y'
}

note_updated_body = {
    'body': 'this is an updated note'
}

tag_body = {
    'tag': 'cheese'
}

tag_body_2 = {
    'tag': 'ham'
}
