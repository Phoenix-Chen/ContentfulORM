from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='contentful_orm',
    version='0.0.1',
    author='Phoenix Chen',
    author_email='',
    packages=['contentful_orm', 'contentful_orm.fields'],
    scripts=[],
    description='',
    long_description=long_description,
    install_requires=[
        'contentful_management',
        'python-baseconv'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
