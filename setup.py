from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in file_transfer_engine/__init__.py
from file_transfer_engine import __version__ as version

setup(
	name="file_transfer_engine",
	version=version,
	description="This File Transfer Engine will be used to transfer file from Source system to Destination system",
	author="Hephzibah Technolofies Inc",
	author_email="david.alexander@hephzibahtech.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
