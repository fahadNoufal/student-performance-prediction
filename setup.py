from setuptools import setup, find_packages
from typing import List


def get_requirements(path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    with open(path) as file:
        requirements = file.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        
        if "-e ." in requirements:
            requirements.remove("-e .")
    
    return requirements

setup(
    name ="student performance prediction",
    version ="0.0.1",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt"),
    author = 'Fahad Noufal',
    # install_requires = [],
)
