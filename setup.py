from setuptools import setup


setup(
    name="ipython-gremlin",
    version="0.0.3",
    license="MIT",
    author="davebshow",
    author_email="davebshow@gmail.com",
    url='https://github.com/davebshow/ipython-gremlin',
    description="Runs scripts agains the Gremlin Server from IPython",
    long_description=open("README.txt").read(),
    packages=["gremlin", "tests"],
    install_requires=[
        "aiogremlin==0.0.9"
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
