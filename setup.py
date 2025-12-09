from setuptools import setup, find_packages

setup(
    name='spacy-rup',
    version='0.2.0',
    description='Aromanian language support for spaCy',
    author='Aromanian NLP Project',
    packages=find_packages(),
    install_requires=[
        'spacy>=3.0.0',
    ],
    entry_points={
        'spacy_languages': [
            'rup = spacy_rup:Aromanian',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Romanian',
    ],
)
