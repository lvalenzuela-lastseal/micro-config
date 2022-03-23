from setuptools import setup

setup(
    name="micro-config",
    version="1.1.1",
    description="Módulo que mantiene configuraciones estandar para micro servicios",
    author="Lastseal",
    author_email="hello@lastseal.com",
    url="https://www.lastseal.com",
    packages=['micro'],
    install_requires=[ 
        i.strip() for i in open("requirements.txt").readlines() 
    ]
)
