from setuptools import setup, find_packages

def get_req(filepath):
    """this func will return list of required packages"""
    requirements = []
    with open(filepath) as fileobj:
        requirements=fileobj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
        
    if '-e .' in requirements:
        requirements.remove('-e .')
        
    return requirements    

setup(
    name='mlproject',               # Name of the package
    version='0.1',                  # Package version
    long_description=open('README.md').read(),  # Detailed description from README
    author='Jayesh Patil',            # Author's name
    author_email='jayeshps0134@gmail.com',  # Author's email address
    packages=find_packages(),       # Automatically find packages in the directory
    install_requires=get_req('requirements.txt')              # List of dependencies
)
