from setuptools import setup

setup(
    name='runcalc',
    version='0.1.1',
    description='Running pace calculator',
    author='Mike Patek',
    author_email='mpatek@gmail.com',
    url='https://github.com/mpatek/runcalc',
    download_url='https://github.com/mpatek/runcalc/tarball/0.1',
    packages=['runcalc'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'runcalc=runcalc.cli:cli'
        ]
    },
    install_requires=['click'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords=['running', 'exercise', 'cli'],
)
