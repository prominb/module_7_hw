from setuptools import setup


setup(name='clean_folder',
      version='0.0.1',
      description='Very usefull code',
      url='http://github.com/storborg/usefull',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['clean_folder'],
      install_requires=[
                        'markdown',
                        ],
      entry_points={
                    'console_scripts': ['clean-folder = clean_folder.clean:main']
                    },
      zip_safe=False)