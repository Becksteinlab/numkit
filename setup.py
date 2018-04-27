#! /usr/bin/python
"""Setuptools-based setup script for numkit.

For a basic installation just type the command::

  python setup.py install

"""

from setuptools import setup, find_packages
import versioneer

setup(name='numkit',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='numerical first aid kit',
      author='Oliver Beckstein',
      author_email='orbeckst@gmail.com',
      url = 'https://github.com/Becksteinlab/numkit',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      scripts=[],
      license='BSD',
      long_description=open('README.rst').read(),
      tests_require = ['numpy>=1.9', 'pytest'],
      install_requires=['numpy>=1.9', 'scipy>=1.0', 'six']
)
