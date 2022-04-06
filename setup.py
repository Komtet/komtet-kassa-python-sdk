from setuptools import find_packages, setup


with open('README.rst', 'r') as readme:
    long_description = readme.read()

with open('CHANGELOG.rst', 'r') as changelog:
    long_description += '\n\n' + changelog.read()

setup(
    name='komtet_kassa_sdk',
    version='7.0.2',
    license='MIT',
    description='Python SDK for KOMTET Kassa',
    long_description=long_description,

    author='Motmom',
    author_email='motmom.dev@gmail.com',

    maintainer='Guryev Konstantin',
    maintainer_email='kosmini4@gmail.com',

    url='https://github.com/Komtet/komtet-kassa-python-sdk',
    download_url='https://pypi.python.org/pypi/komtet_kassa_sdk',

    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=[
        'requests'
    ]
)
