from setuptools import setup


setup(
    name="aland20-utils",
    version="0.2.0",
    py_modules=["quick_utils"],
    install_requires=[
        "cryptography",
        "requests",
        "pymysql",
        "cassandra-driver",
    ],
    description="A collection of utility functions for quick scripting",
    author="AlanD20",
    author_email="aland20@pm.me",
    url="https://github.com/aland20/pytils",
    license="MIT",
)
