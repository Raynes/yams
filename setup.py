from setuptools import setup, find_packages

setup(
    name="yams",
    version="0.1.0",
    author="Anthony Grimes",
    author_email="yams@raynes.me",
    include_package_data=True,
    url="https://github.com/Raynes/yams",
    install_requires=[
        'rxv==0.1.9'
    ],
    packages=find_packages()
)
