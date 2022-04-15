from appsample.model import User


def test_login_page(test_client):
    response = test_client.get('/zh/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data


def test_valid_login_logout(test_client):
    response = test_client.post('/zh/login', data={'account': 'admin', 'password': 'admin'})
    assert response.status_code == 200


def test_register_and_login(test_client):
    # register a new account
    response = test_client.post('/zh/signup', data={
        'email': 'john@example.com',
        'username': 'john',
        'account': 'cat',
        'password': 'cat',
        'password2': 'cat'
    })
    assert response.status_code == 200

    # login with the new account
    response = test_client.post('/zh/login', data={
        'email': 'john@example.com',
        'password': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200

    # send a confirmation token
    user1 = User.query.filter_by(email='john@example.com').first()
    token = user1.generate_confirmation_token()
    response = test_client.get('/zh/confirm/{}'.format(token), follow_redirects=True)
    user1.confirm(token)
    assert response.status_code == 200
    assert 'You have confirmed your account' in response.get_data(as_text=True)

    # log out
    response = test_client.get('/zh/logout', follow_redirects=True)
    assert response.status_code == 200
