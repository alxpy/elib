CSRF_ENABLED = True
SECRET_KEY = 'JHGJH45#%@#)h#ghGJHGJhg#jhg@$hjG'

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = 'sqlite:///sqlite.db'

# RECAPTCHA_PUBLIC_KEY = '#############'