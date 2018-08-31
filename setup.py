from distutils.core import setup

setup(
    name='Article2TVNews',
    version='0.1.0',
    author='Max W. Reinisch',
    author_email='reinischmax@gmail.com',
    packages=['article2tvnews', 'article2tvnews.test'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='https://github.com/MaxReinisch/article2tvnews-package',
    license='LICENSE.txt',
    description='Recommends TV news clips related to given news articles',
    long_description=open('README.txt').read(),
    install_requires=[
        "lxml==4.2.4",
        "numpy==1.15.0",
        "readability-lxml==0.7",
        "requests==2.19.1",
        "scikit-learn==0.19.2",
        "scipy==1.1.0",
        "sklearn==0.0",
        "urllib3==1.23"
    ],
)
