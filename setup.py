from setuptools import setup
import os


if os.path.isfile('requirements.txt'):
    with open('requirements.txt', 'r') as requirements_file:
        install_requires = requirements_file.read().splitlines()

setup(
    name='metaboscape_database_downloader',
    version='0.1.0',
    url='https://github.com/gtluubruker/metaboscape_database_downloader',
    license='MIT License',
    author='Gordon T. Luu',
    author_email='gordon.luu@bruker.com',
    packages=['mdd'],
    description='A simple GUI to download publicly available databases for use with the annotation tool in MetaboScape.',
    entry_points={'console_scripts': ['metaboscape_database_downloader=mdd.gui:main']},
    install_requires=install_requires,
    setup_requires=install_requires
)
