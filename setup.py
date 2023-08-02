from setuptools import setup, find_packages
import os


def requirements():
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), 'r') as f:
        return [line.strip() for line in f.readlines()]


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), 'r') as f:
        return f.read()


setup(
    name='smshub_py',
    version='1.0.0',
    license='MIT',
    description="API wrapper for SmsHub",
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[*requirements()]
)
