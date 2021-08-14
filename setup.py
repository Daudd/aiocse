import setuptools

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = ""
with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name = 'aiocse',
    version = '1.0.1',
    description = 'A Python wrapper for the Google Custom Search JSON API.',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Daudd/aiocse',
    author = 'Daud',
    license = 'MIT',
    packages = setuptools.find_packages(),
    install_requires = requirements,
)