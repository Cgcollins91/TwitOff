from setuptools import setup

setup(
    name='TwitOff',
    version='1.0',
    long_description=__doc__,
    packages=['twitoff'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)