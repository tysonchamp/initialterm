# your_project_directory/setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="initialterm",
    version="0.1.0",
    author="Sujith S",
    author_email="sujith@zackriya.com",
    description="A human to command-line innterface tool powered by LLM models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/sujith/your-repo-name",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[  # List the dependencies of this project here.
        'ollama',  # Replace with actual dependency
        'requests'  # If your code uses requests, add it here.
    ],
    entry_points={
        'console_scripts': [
            'initialterm=initialterm.main:start_custom_cmd',
        ],
    }

)
