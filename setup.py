from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="autotests-coverage",
    version="1.0.0",
    author="Jamal Zeinalov",
    author_email="jamal.zeynalov@gmail.com",
    description='Python adapter for "swagger-coverage" tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamalZeynalov/swagger-coverage-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests==2.32.0",
        "setuptools==70.0.0",
        "PyYAML>=6.0",
        "pydantic==2.6.1",
        "filelock>=3.11.0"
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
