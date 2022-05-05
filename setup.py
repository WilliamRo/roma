from roma import console
from setuptools import setup, find_packages


# Specify version
VERSION = '1.0.0.dev8'


# Preprocess
console.show_status('Running setup.py for roma-v' + VERSION + ' ...')
console.split('-')


# Run setup
def readme():
  with open('README.md', 'r') as f:
    return f.read()

# Submodules will be included as package data, specified in MANIFEST.in
setup(
  name='py-roma',
  packages=find_packages(),
  include_package_data=True,
  version=VERSION,
  description='A python development kit containing handy packages.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  author='William Ro',
  author_email='luo.wei@zju.edu.cn',
  url='https://github.com/WilliamRo/roma',
  download_url='https://github.com/WilliamRo/roma/tarball/v' + VERSION,
  license='Apache-2.0',
  keywords=['utilities', 'console', 'checker'],
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Utilities",
  ],
)
