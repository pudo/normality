from setuptools import setup


setup(
    name='normality',
    version='0.3.0',
    description="Micro-library to normalize text strings",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3'
    ],
    keywords='text unicode normalization slugs',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/pudo/normality',
    license='MIT',
    py_modules=['normality'],
    namespace_packages=[],
    include_package_data=False,
    zip_safe=True,
    install_requires=[
        'six'
    ],
    tests_require=[],
    test_suite='test',
    entry_points={
    }
)
