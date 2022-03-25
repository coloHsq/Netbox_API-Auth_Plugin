from setuptools import setup, find_packages


setup(
    name='auth-api',
    version='1.0',
    description='Custom encrypted api authentication',
    url='https://github.com/coloHsq/Netbox_API-Auth_Plugin',
    author='Davide Colombo',
    author_email='colombo.davidehsq@gmail.com',
    license='MIT',
    install_requires=['pycryptodome'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)

