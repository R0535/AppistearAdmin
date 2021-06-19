from threading import current_thread
from flask.helpers import url_for
from flask_testing import TestCase
from flask import  current_app
from main import app
class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING']= True
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def test_app_exists(self):
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'],True)

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response,url_for('auth.login'))

    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)
    

    def test_login_post(self):
        fake_form = {
            'username':'fake',
            'password':'fake',
        }
        response = self.client.post(url_for('auth.login'),data =fake_form)
        self.assertRedirects(response,url_for('home'))

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)
    
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)
        
    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')
