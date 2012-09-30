"""
Flask-Gears
-----------

Gears_ for Flask_.

.. _Gears: https://github.com/gears/gears
.. _Flask: http://flask.pocoo.org/
"""
from setuptools import setup


setup(
    name='Flask-Gears',
    version='0.1.2',
    url='https://github.com/gears/flask-gears',
    license='ISC',
    author='Mike Yumatov',
    author_email='mike@yumatov.org',
    description='Gears for Flask',
    long_description=__doc__,
    py_modules=['flask_gears'],
    platforms='any',
    install_requires=[
        'Flask',
        'Gears',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
