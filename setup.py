from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1'
DESCRIPTION = 'Manage Mesh Structured.'
PACKAGE_NAME = 'MeshStructured'
AUTHOR = 'IHCantabria - AGV'
EMAIL = 'gonzalezva@unican.es'
GITHUB_URL = 'https://github.com/alexgonzvalle'

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license='',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    keywords=[],
    install_requires=[
        'matplotlib', 'scipy'
    ],
    package_data={},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)