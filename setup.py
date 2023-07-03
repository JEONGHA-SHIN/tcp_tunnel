from setuptools import setup, find_packages

setup(
    name='tcp_tunnel',
    version='1.0.0',
    description='TCP Tunnel Application',
    author='Jeongha, Shin',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pytunnel',
    ],
)
