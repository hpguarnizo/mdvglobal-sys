from .base import *
import dj_database_url

#Email default hola@company.com
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

#Email soporte@company.com
EMAIL_HOST_USER_SOPORTE = os.environ.get('EMAIL_HOST_USER_SOPORTE')
EMAIL_HOST_PASSWORD_SOPORTE = os.environ.get('EMAIL_HOST_PASSWORD_SOPORTE')

#Email finanzas@company.com
EMAIL_HOST_USER_FELICIDAD= os.environ.get('EMAIL_HOST_USER_FELICIDAD')
EMAIL_HOST_PASSWORD_FELICIDAD = os.environ.get('EMAIL_HOST_PASSWORD_FELICIDAD')


#Segure
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

ADMINS=[('Support', EMAIL_HOST_USER_SOPORTE)]

ALLOWED_HOSTS = ['www.tudominio.com',]

INSTALLED_APPS += [
     'django.contrib.staticfiles',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#Facebook Keys
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]
SOCIAL_AUTH_USER_MODEL = 'accounts.MyUser'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

#Twitter keys
SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')

#Google keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

#Redirect login
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/share/user/all"

AUTHENTICATION_BACKENDS = (
    # Facebook
    'social_core.backends.facebook.FacebookOAuth2',
    # Twitter
    'social_core.backends.twitter.TwitterOAuth',
    # Google
    'social_core.backends.google.GoogleOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# AWS keys
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# The region of your bucket, more info:
# http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
S3DIRECT_REGION = os.environ.get('S3DIRECT_REGION')

# Destinations, with the following keys:
#
# key [required] Where to upload the file to, can be either:
#     1. '/' = Upload to root with the original filename.
#     2. 'some/path' = Upload to some/path with the original filename.
#     3. functionName = Pass a function and create your own path/filename.
# auth [optional] An ACL function to whether the current Django user can perform this action.
# allowed [optional] List of allowed MIME types.
# acl [optional] Give the object another ACL rather than 'public-read'.
# cache_control [optional] Cache control headers, eg 'max-age=2592000'.
# content_disposition [optional] Useful for sending files as attachments.
# bucket [optional] Specify a different bucket for this particular object.
# server_side_encryption [optional] Encryption headers for buckets that require it.

def create_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('custom', filename)


S3DIRECT_DESTINATIONS = {
    # Allow anybody to upload any MIME type
    os.environ.get('AWS_STORAGE_BUCKET_NAME'): {
        'key': '/'
    },

    #  Allow staff users to upload any MIME type
    # 'pdfs': {
    #     'key': 'uploads/pdfs',
    #     'auth': lambda u: u.is_staff
    # },

    # Allow anybody to upload jpeg's and png's. Limit sizes to 5kb - 20mb
    'images': {
        'key': 'uploads/images',
        'auth': lambda u: True,
        'allowed': [
            'image/jpeg',
            'image/png'
        ],
        'content_length_range': (5000, 20000000),
    },

    # # Allow authenticated users to upload mp4's
    # 'videos': {
    #     'key': 'uploads/videos',
    #     'auth': lambda u: u.is_authenticated(),
    #     'allowed': ['video/mp4']
    # },

    # Allow anybody to upload any MIME type with a custom name function
    'custom_filename': {
        'key': create_filename
    },
}


