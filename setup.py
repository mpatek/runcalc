from setuptools import setup

setup(
    name='runcalc',
    version='0.1',
    description='Running pace calculator',
    author='Mike Patek',
    author_email='mpatek@gmail.com',
    url='https://github.com/mpatek/runcalc',
    packages=['runcalc'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'runcalc=runcalc.cli:cli'
        ]
    },
    setup_requires=['pytest-runner','click'],
    tests_require=['pytest'],
)
