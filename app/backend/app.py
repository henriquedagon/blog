######################################################################################
# imports

# flask imports
from flask import (
    Flask, 
    request, 
    make_response, 
    Blueprint, 
#     jsonify, 
    abort,
    send_from_directory
)

from flask_restplus import (
    Api, 
    Resource,
    fields
)

from werkzeug.datastructures import FileStorage
from flask_cors import CORS, cross_origin
from functools import wraps
import logging 
import logging.config
from jwt import ExpiredSignatureError, InvalidTokenError

# auxiliary libs
import json
import psycopg2
from PIL import Image
import os
from datetime import datetime
import pandas as pd
import traceback

# my libs
import auth
import backend

######################################################################################
# constants
UPLOAD_DIRECTORY = './images'
ADMIN_GROUP = '2'

######################################################################################
# flask logging

logging.config.dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'formatter': 'default',
        'filename': './logs/blog_api.log'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

log = logging.getLogger('root')

######################################################################################
# flask init

app = Flask('SuperSimBlogAPI')
CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(version='1.0', title='SuperSim Blog Model Rest API',
          description='Manages posts at SuperSim Blog')

blog_api_ns = api.namespace('api', description='Blog API')

def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_api_ns)
    flask_app.register_blueprint(blueprint)

posts_table = backend.Posts(backend.conn_str())
users_table = backend.Users(backend.conn_str())

# create image dir
if not os.path.isdir(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

initialize_app(app)

######################################################################################
# parsers and models
add_post_parser = api.parser()
add_post_parser.add_argument('title', type=str, help='Title of the post', location='form', required=True)
add_post_parser.add_argument('post', type=str, help='Post text', location='form', required=True)
add_post_parser.add_argument('categories', type=str, help='categories separated by comma', location='form', required=True)
add_post_parser.add_argument('author', type=str, help='Author of the post', location='form', required=True)
add_post_parser.add_argument('image', type=FileStorage, location='files', help='Image of the post', required=True)
add_post_parser.add_argument('token', type=str, location='headers', help='Authentication token', required=True)

#----------------------------------------------
get_token_200 = api.model('get_token_200', {
    'token': fields.String,
})

get_token_401 = api.model('get_token_401', {
    'authorization': fields.Boolean,
})
#----------------------------------------------
add_post_200 = api.model('add_post_200', {
    'status': fields.String,
})

add_post_400 = api.model('add_post_400', {
    'error': fields.String,
})
#----------------------------------------------
posts_fields = api.model('posts_fields',{
            'title': fields.String,
            'post': fields.String,
            'categories': fields.String,
            'img_filename': fields.String,
            'image_name': fields.String,
            'author': fields.String,
            'date': fields.String,
})

posts_200 = api.model('posts_200', {
    'data': fields.List(fields.Nested(posts_fields))
})
######################################################################################
# functions and classes
def authenticate(permitted_groups):
    def permissioning(f):
        @wraps(f)
        def decorated_function(self, *args, **kwargs):
            token = request.headers.get('token')
            error = {}

            log.debug('***authentication***')
            log.debug(f'token:{token}')

            try:
                credentials = auth.decode_auth_token(token)
                if (credentials['grp'] not in permitted_groups):
                    abort(403, description='Unauthorized user')
            except ExpiredSignatureError:
                error['token'] = 'expired'
            except InvalidTokenError:
                error['token'] = 'invalid'
            except Exception as e:
                error['error'] = f'{traceback.format_exc()}'
                log.debug('authentication error')
                log.debug(str(traceback.format_exc()))
                raise e
            finally:
                if len(error) > 0:
                    abort(400, description=error)
            log.debug('***authentication end***')
            return f(self, error, credentials, *args, **kwargs)
        return decorated_function
    return permissioning

######################################################################################
# endpoints
@app.route('/')
def home():
    return 'Blog Rest-API'

@blog_api_ns.route('/get_token/<encrypted_credentials>')
class Auth(Resource):
    @blog_api_ns.doc(description='Check existence of table',
    responses={
        200: ("Succeeded", get_token_200),
        401: ("Unauthenticated", get_token_401),
        500: "Internal server error"
    })

    def get(self, encrypted_credentials):

        error = {}

        log.debug(f'encrypted_credentials: {encrypted_credentials}')
        try:
            credentials = json.loads(auth.decrypt(encrypted_credentials)) 
            verified = users_table.verify(credentials['usr'], credentials['psw'])
            assert(verified), 'unverified user or password'
            token = auth.encode_auth_token( credentials['sys'],
                                            credentials['usr'],
                                            credentials['psw'],
                                            credentials['grp'])
            log.debug(f'credentials: {credentials}, verified: {verified}')
            
        except Exception as e:
            error['authorization'] = str(e)
        finally:
            if len(error) > 0:
                abort(401, description=error)
        result = {'token': token}
        log.debug('')
        
        response = make_response(json.dumps(result))
        return response


@blog_api_ns.route('/add_post/')
class AddPost(Resource):
    @blog_api_ns.doc(description='adds a post to database',
    responses={
        200: ("Succeeded", add_post_200),
        400: ("Bad request", add_post_400),
        500: "Internal server error"
    })
    @blog_api_ns.expect(add_post_parser)
    @cross_origin(origin='*', headers=['Access-Control-Allow-Origin', 'Content-Type'])
    @authenticate((ADMIN_GROUP,))
    def post(self, error, credentials):
        try:
            title = request.form.get("title")
            ppost = request.form.get("post")
            categories = request.form.get("categories")
            author = request.form.get("author")
            img_buffer = request.files.getlist('image')[0]
            now_time = datetime.now().strftime('%Y%m%d%H%M%S')
            # now_date = datetime.now().strftime('%Y%m%d')

            print('entrou no add post')
            buffer_filename = f"{now_time}_{img_buffer.filename}"
            img_buffer.save(os.path.join(UPLOAD_DIRECTORY, buffer_filename))

            print('salvou imagem')
            print(title, 
                            ppost, 
                            categories, 
                            buffer_filename, 
                            img_buffer.filename, 
                            author, 
                            now_time)
            posts_table.insert(title, 
                            ppost, 
                            categories, 
                            buffer_filename, 
                            img_buffer.filename, 
                            author, 
                            now_time)
            
            print('inseriu')
            return {'status': 'post ok'}
        except KeyError as e:
            blog_api_ns.abort(400, e.__doc__, status = "Could not save information", 
                                                statusCode = "400")
        except Exception as e:
            blog_api_ns.abort(500, e.__doc__, status = "Could not save information", 
                                                        statusCode = "500")


@blog_api_ns.route('/posts/')
class Posts(Resource):
    @blog_api_ns.doc(description='retrieves posts from database',
    responses={
        200: ("Succeeded", posts_200),
        500: "Internal server error"
    })
    def get(self):
        try:
            data = posts_table.view()
            columns = ['title', 'post', 'categories', 'img_filename', 'image_name', 'author', 'date']
            posts_df = pd.DataFrame(data, columns=columns).astype(str)
            posts_df['date'] = posts_df['date'].apply(lambda d: f'{d[6:8]}/{d[4:6]}/{d[0:4]}')

            response = {
                        'data':posts_df.to_dict('records'),
                       }
            return response

        except Exception as e:
            blog_api_ns.abort(500, e.__doc__, status = "Could not retrieve information",
                                                statusCode = "500")


@blog_api_ns.route('/files/<path>')
class Files(Resource):
    @blog_api_ns.doc(description='retrieves files from database',
    responses={
        200: "Succeeded",
        400: "Bad request",
        500: "Internal server error"
    })
    def get(self, path):
        try:
            return send_from_directory(UPLOAD_DIRECTORY,path)
        except Exception as e:
            blog_api_ns.abort(500, e.__doc__, status = "Could not retrieve information",
                                                statusCode = "500")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')