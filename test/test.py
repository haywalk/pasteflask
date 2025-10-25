import requests
import json

SERVER = 'http://localhost:5000'

def login(user, password):
    '''Log in and return an auth token.
    '''
    # construct data to post
    creds = {
        'username': user,
        'password': password
    }

    # send login request
    resp = requests.post(f'{SERVER}/login',
        headers={
            'Content-Type': 'application/json'
        },
        data=json.dumps(creds))
    
    # read and return token
    token = json.loads(resp.text)['token']
    return token

def upload(token, paste):
    '''Upload a paste.
    '''

    resp = requests.post(f'{SERVER}/paste',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        data=json.dumps(paste))

    return resp.text

def retrieve(id):
    '''Retrieve a paste.
    '''

    resp = requests.get(f'{SERVER}/retrieve/{id}')
    return json.loads(resp.text)

if __name__ == '__main__':
    # log in
    token = login('testuser', 'testpass')
    print(f'logged in. token:\n\t{token}\n')


    to_post = {
        'title': 'asdf',
        'content': 'hello world'
    }

    id = upload(token, to_post)
    print(f'pasted successfully. id: {id}\n')

    paste = retrieve(id)
    print(f'retrieved paste:')
    print(paste)
