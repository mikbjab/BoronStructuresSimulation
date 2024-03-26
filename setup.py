import setuptools
from setuptools import setup

setup(
    name='Simulation of atoms',
    version='1.0',
    packages=setuptools.find_packages(),
    python_requires='>=3',
    install_requires=['numpy', 'matplotlib'],
    url='',
    license='',
    author='Mikołaj Jabłoński',
    author_email='miko9860@gmail.com',
    description='Simulation of one layers of atoms with given energy function dependent on number of neighbors'
)
