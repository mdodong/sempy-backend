from setuptools import setup, find_packages

setup(name='sempy-backend',
      version='0.01',
      description='Backend Server for Sempy the semux python light wallet',
      url='http://github.com/mdodong/sempy-backend',
      author='mdodong',
      license='MIT',
      install_requires=[
          'flask',
          'flask-cors',
          'requests',
          'connexion'
      ],
      zip_safe=False)
