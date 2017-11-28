from setuptools import setup

exec (open('dash_components/version.py').read())

setup(
    name='dash_components',
    version=__version__,
    author='CityofToronto',
    packages=['dash_components'],
    include_package_data=True,
    license='MIT',
    description='Components for King Street Pilot Dashboard',
    install_requires=[]
)
