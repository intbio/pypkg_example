from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

version_file = open(os.path.join(here, 'VERSION'))
version = version_file.read().strip()



setup(
    name="pypkg_example", #TODO
    packages=find_packages(exclude=['examples', 'docs', 'tests*']),

    # Versions should comply with PEP440. For single-sourced versioning, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    description='An example python package', #TODO
    long_description='Long description if needed ... ', #TODO

    # The project URL.
    url='https://github.com/intbio/pypkg_example', #TODO

    # Author details
    author='Alexey K. Shaytan', #TODO
    author_email='alex@intbio.org',#TODO

    # Choose your license
    license='GPL', #TODO

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # Project maturity. 
        'Development Status :: 3 - Alpha', #TODO

        # Intended audience
        'Intended Audience :: Science/Research', #TODO

        # Topic
        'Topic :: Scientific/Engineering :: Bio-Informatics', #TODO

        # License should match "license" above
        'License :: GPL', #TODO

        # Python versions supported
        'Programming Language :: Python :: 3.1', #TODO
    ],

    # What does your project relate to?
    keywords=[], #TODO list of keywords

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().

    # Run-time package dependencies. These will be installed by pip when your
    # project is installed.
    install_requires=[
        'numpy>=1.11.0', #TODO
    ],
  
  #  extras_require = {
  #  'pred': [
  #      'Cython',
  #  ],},

    # Data files included in your packages. If using Python 2.6 or less, 
    # then these have to be included in MANIFEST.in as well.
    include_package_data=True, #If using the setuptools-specific include_package_data argument, files specified by package_data will not be automatically added to the manifest unless they are listed in the MANIFEST.in file. To access data see https://setuptools.readthedocs.io/en/latest/pkg_resources.html#resourcemanager-api

    # package_data={
    #    'hydroid': ['pkgdata/amber10_rmin.config','pkgdata/charmm36_rmin.config','pkgdata/cnr.otf','pkgdata/cnrb.otf'],
    #},

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
         'console_scripts': [ #Creating two console scripts called foo and bar
            'foo = expkg.moda:exfunc', #TODO
            'bar = expkg.modb:exfunc', #TODO
        ]
    },
    python_requires='>=3', #TODO

    # Default to False unless you specifically intend the package to be
    # installed as an .egg
    zip_safe=False,
)
