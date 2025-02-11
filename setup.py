from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="swagger-coverage-metrics",
    version="0.0.2-alpha.1",
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
        "python-dotenv>=0.21.0",
        "rootpath==0.1.0",
        "environs>=9.5.0",
        "filelock==3.17.0"
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
