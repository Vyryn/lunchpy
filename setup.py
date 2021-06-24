from setuptools import setup

setup(
    name='lunchpy',
    version='0.0.1',
    author='Vyryn',
    author_email='vyryn@protonmail.com',
    url='https://github.com/Vyryn/lunchpy',
    description='An API wrapper for Lunch Money',
    packages=['lunchpy'],
    install_requires=[
        'requests~=2.25.1',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Programming Language :: Python :: 3.9',
    ]
)
