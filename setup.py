from setuptools import setup, find_packages


requires = [
    'jsonschema',
    'requests',
    'six'
]

with open('README.rst', 'r') as readme:
    long_description = readme.read()

with open('CHANGELOG.rst', 'r') as changelog:
    long_description += '\n\n' + changelog.read()

setup(
    name='komtet_kassa_sdk',
    version='0.1.0',
    license='MIT',
    keywords=['online kassa', 'sdk'],
    description='Python SDK for OnlineKacca',
    long_description=long_description,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Motmom',
    author_email='motmom.dev@gmail.com',
    maintainer='Guryev Konstantin',
    maintainer_email='kosmini4@gmail.com',
    install_requires=requires,
    url='https://github.com/Motmom/komtet-kassa-python-sdk',
    download_url='https://pypi.python.org/pypi/komtet_kassa_sdk',
    include_package_data=True,
    zip_safe=False,
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
    test_suite='tests'
)
