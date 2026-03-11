"""
Setup configuration for copilot-history-pdf package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = ""
readme_path = this_directory / "README.md"
if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='copilot-history-pdf',
    version='0.1.2',
    author='Oliver Benton',  # Update with your name
    author_email='oliver.benton@icloud.com',  # Update with your email
    description='Convert GitHub Copilot chat history JSON files to formatted PDF documents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Oliver1811/copilot-history-pdf',
    project_urls={
        'Bug Reports': 'https://github.com/Oliver1811/copilot-history-pdf/issues',
        'Source': 'https://github.com/Oliver1811/copilot-history-pdf',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Topic :: Education',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='copilot github pdf chat-history education documentation',
    python_requires='>=3.7',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'copilot-to-pdf=copilot_history_pdf.main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
