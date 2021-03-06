from setuptools import setup

from lunchpy import __version__, __title__, __author__, __license__

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=f'{__author__}@protonmail.com',
    url=f'https://github.com/{__author__}/{__title__}',
    description='An API wrapper for Lunch Money',
    packages=[__title__],
    package_data={
        __title__: ['py.typed']
    },
    install_requires=[
        'requests>=2.25.1',
    ],
    license=__license__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.9',
    ]
)
