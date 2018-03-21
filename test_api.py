import pytest
from app import app

class TestCase():
    ''' Group multiple tests in a class '''

    def test_landing(self):
        ''' Test suite for landing page '''
        with app.test_client() as c:
            response = c.get('/', follow_redirects=True)
            assert response.status_code == 200

    def test_add_task(self):
        ''' Test suite for add new task '''
        with app.test_client() as c:
            response = c.post('/add', follow_redirects=True, data= dict(todoitem="Test task",todoitemdate="7/12/2018"))
            assert response.status_code == 200

    def test_add_sub_task(self):
        ''' Test suite for add new sub task '''
        with app.test_client() as c:
            response = c.post('/addsubtask/3', follow_redirects=True, data= dict(todoitem="Test sub task",todoitemdate="7/12/2018"))
            assert response.status_code == 200

    def test_complete_task(self):
        ''' Test suite for mark as complete task api '''
        with app.test_client() as c:
            response = c.get('/complete/4', follow_redirects=True)
            assert response.status_code == 200

    def test_complete_sub_task(self):
        ''' Test suite for mark as complete sub task api '''
        with app.test_client() as c:
            response = c.get('/completesubtask/5', follow_redirects=True)
            assert response.status_code == 200

    def test_delete__task(self):
        ''' Test suite for delete task  api '''
        with app.test_client() as c:
            response = c.get('/delete/1', follow_redirects=True)
            assert response.status_code == 200

    def test_delete_sub_task(self):
        ''' Test suite for delete sub task  api '''
        with app.test_client() as c:
            response = c.get('/deletesubtask/11', follow_redirects=True)
            assert response.status_code == 200
