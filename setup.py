import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cncd_library',
    version='0.0.1',
    author='Farrukh Khan',
    author_email='farrukh_bala@hotmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Farrukhbala/cncd_library',
    project_urls = {
        "Bug Tracker": "https://github.com/Farrukhbala/cncd_library/issues"
    },
    license='MIT',
    packages=['cncd_library'],
    install_requires=['requests'],
)
