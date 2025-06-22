'''this setup.py is an essential part of packaging and distributing python projects.
it is used by setuptools(or distutils in older python versions) to define the configuration of ur project,such as its metadata,dependencies,and more'''

from setuptools import find_packages,setup #sare folder ko scan krega jhan bhi __init__ file hoyega use package khega
from typing import List

def get_requirements()->List[str]: #returns list
    '''
    this function will return list of requirements
    '''
    requirement_lst:List[str]=[]

    try:
        with open('requirements.txt','r') as file:
            ##read lines from file
            lines=file.readlines()
            ##process each lines:
            for line in lines:
                requirement=line.strip()
                ##ignore empty lines and -e.
                if requirement and not requirement.startswith('-e'):#Matlab:👉 Agar line khaali nahi hai aur👉 line -e . nahi hai tabhi usse requirement_lst me daalo.
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

print(get_requirements())

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Shweta yadav",
    packages=find_packages(),
    install_requires=get_requirements()
)