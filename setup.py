from distutils.core import setup

setup(
    name = 'configurator',
    packages = ['configurator'], # this must be the same as the name above
    version = '0.1',
    description = 'A library for easy configuration',
    author = 'Charles Smith, Jeff Magnusson',
    author_email = 'charsmith@gmail.com, magnussj@gmail.com',
    url = 'https://github.com/charsmith/configurator', # use the URL to the github repo
    download_url = 'https://github.com/charmsith/configurator/tarball/0.1', # I'll explain this in a second
    keywords = ['configuration', 'ini'], # arbitrary keywords
    license = 'Apache Software License',
    classifiers = [
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
    ],
)
