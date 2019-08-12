from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='contentful_orm',
    version='0.0.1',
    author='Phoenix Chen',
    author_email='',
    packages=['contentful_orm'],
    scripts=[],
    # url='',
    # license='LICENSE.txt',
    description='',
    long_description=long_description,
    install_requires=[
        'contentful_management',
        'python-baseconv'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ]
)
