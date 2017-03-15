from setuptools import setup


setup(
    name="ipython-gremlin",
    version="1.0.0b1",
    license="MIT",
    author="davebshow",
    author_email="davebshow@gmail.com",
    url='https://github.com/davebshow/ipython-gremlin',
    description="Runs scripts agains the Gremlin Server from IPython",
    long_description=open("README.txt").read(),
    packages=["gremlin"],
    install_requires=[
        "aiogremlin==3.2.4b2",
        "ipython==5.3.0"
    ],
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
