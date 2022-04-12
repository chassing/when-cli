import time

from setuptools import setup

setup(
    name="when-cli",
    version=int(time.time()),
    description="WHEN Command Line Interface",
    author="Christian Assing",
    author_email="chris@ca-net.org",
    url="https://github.com/chassing/when-cli",
    packages=[
        "when",
    ],
    package_dir={"when": "when"},
    include_package_data=True,
    install_requires=[],
    license="Public Domain (WTFPL)",
    platforms="any",
    keywords="when",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    test_suite="tests",
)
