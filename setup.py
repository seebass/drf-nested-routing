# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='drf-nested-routing',
    version="0.9.6",
    url='https://github.com/seebass/drf-nested-routing',
    license='MIT',
    description='Nested routing extension for Django REST Framework 3',
    author='Sebastian Bredehöft',
    author_email='bredehoeft.sebastian@gmail.com',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'django>=1.6',
        'djangorestframework>=3.4.0',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
