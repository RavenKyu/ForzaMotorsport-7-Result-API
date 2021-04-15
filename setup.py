from setuptools import setup, find_packages

__version__ = '1.0.0b'

LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

tests_require = [
    'pytest',
    'pytest-mock',
]

setup(
    name="forza-result-api",
    version=__version__,
    author="Duk Kyu Lim",
    author_email="hong18s@gmail.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    description='',
    url="https://github.com/RavenKyu/forza_result_api",
    license="MIT",
    keywords=["forza",],
    install_requires=[
    ],
    tests_require=tests_require,
    packages=find_packages(),
    package_data={},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'forza-result-api=forza_result.__main__:main',
        ],
    },
    zip_safe=False,
)
