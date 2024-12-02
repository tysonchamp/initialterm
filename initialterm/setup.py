from setuptools import setup, find_packages

setup(
    name='initialterm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ollama',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'initialterm=main:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A terminal app for executing commands via ollama API.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/initialterm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
