from setuptools import setup

setup(
    name='ToTheGreatOutDoors',
    version='1.0',
    packages=['Django', 'Django.ToTheGreatOutDoors', 'Django.ToTheGreatOutDoors.core',
              'Django.ToTheGreatOutDoors.core.AppViews', 'Django.ToTheGreatOutDoors.core.management',
              'Django.ToTheGreatOutDoors.core.management.commands', 'Django.ToTheGreatOutDoors.core.migrations',
              'Django.ToTheGreatOutDoors.ToTheGreatOutDoors'],
    url='https://github.com/sbaker-dev/ToTheGreatOutDoors',
    license='MIT',
    author='Samuel',
    author_email='samuelbaker.researcher@gmail.com ',
    description='Basic prototype for the JGI competition'
)
