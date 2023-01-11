from setuptools import setup

setup(
    name="pyconfigurator",
    packages=["configurator"],  # this must be the same as the name above
    versioning="post",
    setup_requires="setupmeta",
    install_requires=["future"],
    extras_require={"develop": ["nose", "tox"]},
    description="A library for easy configuration",
    author="Charles Smith, Jeff Magnusson",
    author_email="charles.s.smith@gmail.com, magnussj@gmail.com",
    url="https://github.com/charsmith/configurator",  # use the URL to the github repo
    keywords=["configuration", "ini"],  # arbitrary keywords
    license="Apache Software License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
