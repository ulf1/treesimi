from setuptools import setup
import pypandoc


setup(name='treesimi',
      version='0.1.1',
      description='Compute similarity between netsted set based trees.',
      long_description=pypandoc.convert('README.md', 'rst'),
      url='http://github.com/ulf1/treesimi',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['treesimi'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.6',
      zip_safe=True)
