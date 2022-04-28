# type: ignore

from setuptools import find_packages, setup

setup(
    name='eth_retry',
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    description='Provides a decorator that automatically catches known transient exceptions that are common in the Ethereum/EVM ecosystem and reattempts to evaluate your decorated function',
    author='BobTheBuidler',
    author_email='bobthebuidlerdefi@gmail.com',
    url='https://github.com/BobTheBuidler/eth_retry',
    license='MIT',
    setup_requires=[
        'setuptools_scm',
    ],
)