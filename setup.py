from setuptools import setup
import m2r


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='treesimi',
      version='0.1.0',
      description='Compute similarity between trees, e.g. dependency trees',
      long_description=m2r.parse_from_file('README.md'),
      long_description_content_type='text/x-rst',
      url='http://github.com/ulf1/treesimi',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['treesimi'],
      install_requires=[
          'setuptools>=40.0.0'],
      python_requires='>=3.6',
      zip_safe=False)