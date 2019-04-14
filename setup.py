from setuptools import find_packages, setup

setup(
    name='maglearn-back',
    version='0.0.1',
    packages=find_packages(),
    include_package_date=True,
    zip_safe=False,
    install_requires=[
        'flask', 'graphene'
    ],
)
