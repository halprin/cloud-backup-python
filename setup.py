from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', 'r') as read_me:
        long_description = read_me.read()
        return long_description


def get_requirements():
    requirements = open('requirements.txt').read()
    return [r for r in requirements.strip().splitlines()]


setup(
    name='cloud-backup',
    version='1.0.0',
    author='halprin',
    author_email='me@halprin.io',
    description='Simple cloud backup solution utilizing AWS KMS and S3',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/halprin/cloud-backup',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
    ],
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        cloud-backup=backup.cli.main:cli
    ''',
)
