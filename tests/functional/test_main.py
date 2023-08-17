from appsample.model import User


def test_login_page(test_client):
    response = test_client.get('/zh/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data


def test_register_and_login(test_client, celery_mock):
    # 註冊(用mock取代celery)
    response = test_client.post('/zh/signup', data={'email': 'jason@example.com',
                                                    'username': 'john',
                                                    'account': 'cat',
                                                    'password': 'cat',
                                                    'password2': 'cat'
                                                    }, follow_redirects=True)
    assert response.status_code == 200

    # 登入
    response = test_client.post('/zh/login', data={'account': 'jason@example.com',
                                                   'password': 'cat',
                                                   'submit': 'Login'
                                                   }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid account or password.' not in response.data

    with test_client.session_transaction() as sess:
        sess['user_id'] = 2

    # 使用者確認(token)
    user1 = User.query.filter_by(email='jason@example.com').first()
    token = user1.generate_confirmation_token()
    response = test_client.get(f'/zh/confirm/{token}', follow_redirects=True)

    assert user1.confirm(token)
    assert response.status_code == 200
    assert b'You have confirmed your account. Thanks!' in response.data

    # 登出
    response = test_client.get('/zh/logout', follow_redirects=True)
    assert response.status_code == 200


def test_change_password(test_client):
    response = test_client.post('/zh/login', data={'account': 'admin', 'password': 'admin'})
    assert response.status_code == 200

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    response = test_client.post('/zh/change_password', data={'old_password': "test1",
                                                             'password': 'test1',
                                                             'password2': 'test1',
                                                             'submit': 'Update'
                                                             }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your password has been updated.' in response.data


def test_main(test_client):
    response = test_client.get('/zh/main')
    assert response.status_code == 200

    test_client.post('/zh/login', data={'account': 'test1', 'password': 'test1'})

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    # 更新資料
    response = test_client.post('/zh/main', data={'mid': 1,
                                                  'name': 's',
                                                  'author': 'ss',
                                                  'group': 'sss',
                                                  'url': 'http://127.0.0.1:7860/',
                                                  'pages': '1',
                                                  'submit': 'Send'
                                                  }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Modify Success' in response.data

    # 新增資料
    response = test_client.post('/zh/main', data={'name': 's',
                                                  'author': 'ss',
                                                  'group': 'sss',
                                                  'url': 'http://127.0.0.1:7860/',
                                                  'pages': '1',
                                                  'submit': 'Send'
                                                  }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Insert Success' in response.data

    response = test_client.post(f'/zh/main', data={'mid': 1}, follow_redirects=True)
    assert response.status_code == 200


def test_main_fuzzy(test_client):
    response = test_client.get('/zh/main')
    assert response.status_code == 200

    test_client.post('/zh/login', data={'account': 'test1', 'password': 'test1'})

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    # 模糊搜尋
    response = test_client.post('/zh/fuzzy', json={'input': 'test'})
    assert response.status_code == 200


def test_user(test_client):
    test_client.post('/zh/login', data={'account': 'test1', 'password': 'test1'})

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    response = test_client.get('/zh/user/test1')
    assert response.status_code == 200


def test_user_role(test_client):
    test_client.post('/zh/login', data={'account': 'test1', 'password': 'test1'})

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    response = test_client.get('/zh/UserRole')
    assert response.status_code == 200

    # 更新使用者權限
    response = test_client.post('/zh/UserRole', data={'submit': 'Submit',
                                                      'uid': 1,
                                                      'username': 'test1',
                                                      'userrole': 3}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Update Success' in response.data


def test_user_upload_and_sort(test_client):
    test_client.post('/zh/login', data={'account': 'test1', 'password': 'test1'})

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1

    # 輪詢各種排序方法
    for i in range(6):
        response = test_client.get(f'/zh/user/upload/test1/{i+1}')
        assert response.status_code == 200

    response = test_client.post(f'/zh/user/upload/test1/1', data={'mid': 1}, follow_redirects=True)
    assert response.status_code == 200

    # 更新自己上傳的資料
    response = test_client.post(f'/zh/user/upload/test1/1', data={'mid': 1,
                                                                  'name': 's',
                                                                  'author': 'ss',
                                                                  'group': 'sss',
                                                                  'url': 'http://127.0.0.1:7860/',
                                                                  'pages': '1',
                                                                  'submit': 'Send'
                                                                  }, follow_redirects=True)
    assert response.status_code == 200

    # 刪除自己上傳的資料
    response = test_client.post(f'/zh/user/upload/test1/1', data={'delete': 'Delete',
                                                                  'delete_mid': 1
                                                                  }, follow_redirects=True)
    assert response.status_code == 200
