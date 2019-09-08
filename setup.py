from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='contentful_orm',
    version='0.1.0',
    author='Phoenix Chen',
    author_email='phoenix0722chen@gmail.com',
    description="A Python toolkit for Contentful to let you create/maintain your Content Type and queries in ORM style.",
    packages=['contentful_orm', 'contentful_orm.fields'],
    scripts=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Phoenix-Chen/ContentfulORM',
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
