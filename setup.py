from setuptools import setup

setup(
    name="nearest_correlation",
    packages=[],
    version="1.1.0",
    description="Python versions of nearest correlation matrix algorithms",
    author='Eka',
    author_email='cto@wemteq.com',
    url='https://github.com/wemteqdev/nearest_correlation',
    keywords=['algorithm'],
    install_requires=['numpy>=1.11.3', 'scipy>=0.19.0'],
    include_package_data=True,
    entry_points={'console_scripts': ['nearest_correlation = nearest_correlation.__main__:main']},
    zip_safe=False,
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 1 - Beta'
    ]
)
