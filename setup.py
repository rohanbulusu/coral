from setuptools import find_packages, setup

setup(
	name='coral',
	packages=find_packages(),
	version='1.1',
	description='A mathematical computation and visualization package',
	author='Rohan Bulusu',
	author_email='rohanbulusu@gmail.com',
	license='MIT',
	tests_require=['pytest==4.4.1']
)
