from appsample.model import User


def test_login_page(test_client):
    response = test_client.get('/zh/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data


def test_valid_login_logout(test_client):
    response = test_client.post('/zh/login', data={'account': 'admin', 'password': 'admin'})
    assert response.status_code == 200


def test_register_and_login(test_client, celery_mock):
    # register a new account
    response = test_client.post('/zh/signup', data={
        'email': 'jason@example.com',
        'username': 'john',
        'account': 'cat',
        'password': 'cat',
        'password2': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200

    # login with the new account
    response = test_client.post('/zh/login', data={
        'email': 'jason@example.com',
        'password': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid account or password.' not in response.data

    # send a confirmation token
    user1 = User.query.filter_by(email='jason@example.com').first()
    token = user1.generate_confirmation_token()
    response = test_client.get(f'/zh/confirm/{token}', follow_redirects=True)
    assert user1.confirm(token)
    assert response.status_code == 401

    # log out
    response = test_client.get('/zh/logout', follow_redirects=True)
    assert response.status_code == 401
