from setuptools import setup, find_packages

setup(
    description='An IRC bot for Megworld',
    url='https://github.com/moggers87/salmon',
    author='Jessica Tallon',
    maintainer='Matt Molyneaux',
    maintainer_email='moggers87+git@moggers87.co.uk',
    version='6.1',
    packages=find_packages(),
    include_package_data=True,
    name='megbot',
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        ],
    entry_points={
        'console_scripts':
            ['megbot = megbot.bot:main'],
    },
)
