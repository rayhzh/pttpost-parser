from setuptools import setup


setup(
   name='foo',
   version='0.0.1',
   description='A Python library for collecting articles from ptt website',
   author='rayhzh',
   author_email='ray2012789852@gmail.com',
   packages=['ptt'],
   install_requires=['requests', 'beautifulsoup4'],
)
