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
      project_urls={'Documentation': 'https://numkit.readthedocs.org/',
                    'Issue Tracker': 'https://github.com/Becksteinlab/numkit/issues',
                    'Source': 'https://github.com/Becksteinlab/numkit',
      },
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows ',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      scripts=[],
      license='BSD',
      long_description=open('README.rst').read(),
      long_description_content_type='text/x-rst',
      tests_require = ['pytest'],
      install_requires=['numpy>=1.9', 'scipy>=1.0', 'six']
)
