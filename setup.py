from distutils.core import setup
import setuptools

setup(name='pbnh',
      version='0.2',
      description='A Better Pastebin',
      author='Bryce Handerson, Ethan Madden',
      author_email='maddene@madden.ninja',
      url='https://github.com/bhanderson/pbnh',
      packages=setuptools.find_packages(exclude=['docs', 'tests*']),
      include_package_data=True,
      package_data={'pbnh.app': ['static/*.*', 'static/codemirror/*.*',
                                 'static/codemirror/langs/*', 'templates/*'],
                   },
      install_requires=['docutils',
                        'Flask',
                        'gunicorn',
                        'psycopg2',
                        'python-magic',
                        'pyYAML',
                        'SQLAlchemy',
                        'SQLAlchemy-utils'
                       ],
      tests_require=['nose',
                     'pycurl',
                    ]
     )
