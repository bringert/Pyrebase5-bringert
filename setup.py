from setuptools import setup, find_packages

setup(
    name='Pyrebase5-bringert',
    version='5.0.0',
    url='https://github.com/bringert/Pyrebase5-bringert',
    description='A simple python wrapper for the Firebase API with current deps and support for both service account and user authentication',
    author='bringert',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='Firebase',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.19.1',
        'requests_toolbelt>=0.7.1',
        'gcloud>=0.18.3',
        'oauth2client>=4.1.2',
        'python-jwt>=2.0.1',
        'pycryptodome>=3.6.4'
    ]
)
