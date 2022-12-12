''' subprocess module. '''
from subprocess import run
import setuptools


out = run(['git', 'describe'], capture_output=True, check=False)
if out.returncode:
    VERSION = 'unknown'
else:
    VERSION = out.stdout.decode('utf8').split('-')[0]


setuptools.setup(
    name="TodoApp",
    version=VERSION,
    author="umair khalil",
    author_email="umairkhalil4@gmail.com",
    description="TO-DO flask app",
    long_description="",
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask==2.2.2",
        "Flask-RESTful==0.3.9",
        "SQLAlchemy==1.4.45",
        "flask-httpauth-4.7.0"
    ],
    extras_require={
        'dev': [
           "pylint==2.15.8"
        ]
    }
)
