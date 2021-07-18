from setuptools import setup


setup(
   name='pttpost-parser',
   version='0.0.2',
   description='A Python library for collecting articles from ptt website',
   author='rayhzh',
   author_email='ray2012789852@gmail.com',
   url = 'https://github.com/rayhzh/pttpost-parser',
   packages=['ptt'],
   install_requires=['requests', 'beautifulsoup4', 'tabulate', 'tqdm'],
)
