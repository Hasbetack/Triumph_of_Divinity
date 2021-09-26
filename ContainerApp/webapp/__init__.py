from flask import Flask
from webapp.utils import Content_Loader

Content = Content_Loader()
app = Flask(__name__)

from webapp import routes