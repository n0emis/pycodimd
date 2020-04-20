#!/usr/bin/env python3
"""Setup file for the CodiMD client."""
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name='pycodimd',
    version='0.0.1',
    description='Python client for CodiMD',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/n0emis/pycodimd',
    download_url='https://github.com/n0emis/pycodimd/releases',
    author='n0emis',
    author_email='dev@n0emis.eu',
    license='MIT',
    install_requires=['requests'],
    packages=setuptools.find_packages(),
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
)
