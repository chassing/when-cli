
from setuptools import setup

import time


setup(
    name='when-cli',
    version=int(time.time()),
    description='WHEN Command Line Interface',
    author='Christian Assing',
    author_email='christian.assing@infineon.com',
    url='https://wiki.intra.infineon.com',
    packages=[
        'when-cli',
    ],
    package_dir={'when-cli': 'when-cli'},
    include_package_data=True,
    install_requires=[],
    license="Public Domain (WTFPL)",
    platforms='any',
    keywords='when-cli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
    ],
    test_suite='tests',
)
