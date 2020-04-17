# pypkg_example

![](https://github.com/intbio/pypkg_example/workflows/Testing/badge.svg) - for master branch.

This is an example of creating and developing a python package, packaging it with conda, testing and uploading it to anaconda using CI/GitHub actions.

## Instructions on building your own Python project
- Use this project as template, for simple project the name of the project will be the same as the name of the single package inside (i.e. instead of ```pypkg_example``` you can name the projct folder ```expkg``` in this case).
- Key files you need to modify are:
```
setup.py - set all the fields to relevant marked with TODO sign
VERSION - set to 0.0.1
MANIFEST.in - set line 2
README.md - description of your package for github
LICENSE - this file might be generated automatically with github, see that it matches one in setup.py
conda-recipe/meta.yaml - set all fields mapped with TODO, especially git url(!) and requirements(!) 
docker_test/Dockerfile - modify to create appropriate Dockerimage with required deps for testing, build and push it veia docker_test/README.md
.github/actions/test/Dockerfile - set the path to your test docker container on dockerhub
docker - you can setup the container later for the useres to use you library.
```
- Add ```ANACONDA_USERNAME``` and ```ANACONDA_PASSWORD``` secrets on the Settings page.
- You might not want to use workflows from the very beginning, if so - delete the .github/workflows folder.

## A quick and dirty way of creating a new github repo with via a code snippet
https://github.com/github/hub should be installed
GITHUB_TOKEN env variable set [see here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
```
wget https://raw.githubusercontent.com/intbio/pypkg_example/master/quick_pypkg_setup.sh
bash quick_pypkg_setup.sh PACKAGE_NAME
```


## What's in this example and how it works
- Example of a project struture with packages, modules and data folders.
- Example of test using ```pytest```
- Example of setuptools packaging: ```setup.py```,```VERSION, README.md MANIFEST.in```
- Example of ```conda-recipe```
- Example of GitHub actions workflows:
    - Testing
    - Packaging and pushing to anaconda upon new release
### How it works
- Suggested development flow is [GitHub Flow](https://guides.github.com/introduction/flow/), i.e. develop in feature branches, merge or make pull requests into master.
- Semantic versioning 2.0 should be used, see [here](https://semver.org). NOTE versions in the format e.g.  ```0.0.1```, we use the same git tags but with ```v``` prefix (i.e. ```v0.0.1```).
- As a result of a development one eventually makes a commit to the master branch.
- The testing workflow tests all commits using ```pytest```.
- If the version in ```VERSION``` is incremented, a ```Release_new_version_and_push_to_anaconda.yml``` workflow is triggered wich adds a release tag, publishes a release, packages and pushed to anaconda cloude (this can be switch off - since this is a high level of automation).
- ```Publish_to_conda_upon_release.yml``` is triggered by manual relase (simply tagging does not trigger a release!), the project is packaged and pushed to anaconda, the GitHub encrypted secretes should be configured for this and previous steps to work. 



## Some theory

### Python packages
- see https://python-packaging.readthedocs.io/en/latest/
- Module = a file containing Python definitions and statements
- Packages = a way of structuring Python’s module namespace by using “dotted module names”
- A package is a collection of python modules under a common namespace. In practice one is created by placing multiple python modules in a directory with a special `__init__.py` module (file).
- When the project complexity grows, there may be sub-packages and sub-sub-packages in a deep directory structure. In this case, importing a single item from a sub-sub-package will require executing all __init__.py files met while traversing the tree.
```
project\
    package1\
        __init__.py
        modulea.py
        submodule1.1\
            __init__.py
            moduleb.py
    package2\
        __init__.py
        modulec.py
        submodule1.1\
            __init__.py
            moduled.py
    setup.py
```
- if you have one package the name of the project and package will often be the same.
- When we distribute a project, the name of the project is used to install it (e.g. ```pip install project```), and often project is also called a package. But he actuall importable package will be ```expkg```

### Python setuptools
- The most basic way to make the python packages installable is [setuptools](https://setuptools.readthedocs.io/en/latest/)
- Setuptools is a collection of enhancements to the Python distutils that allow developers to more easily build and distribute Python packages, especially ones that have dependencies on other packages.
- Alongside the python packages we need to include a setup.py script
```
from setuptools import setup, find_packages
setup(
    name="HelloWorld", #this is the name of the project NOT package(s)
    version="0.1",
    packages=find_packages(), #or describe packages individually. Looks like submodules can be also put here 
    
)
```
- here is a more detailed example of setup.py https://github.com/biopython/biopython/blob/master/setup.py
- Auxillary config files that are automatically included :
    - See https://packaging.python.org/guides/using-manifest-in/
    - setup.cfg
    - README.md , .rst, .txt
    - MANIFEST.in
    - After adding the above files to the sdist, the commands in MANIFEST.in (if such a file exists) are executed in order to add and remove further files to & from the sdist.


### Installing packages using setuptools and pip
- ```pip install``` is a command that takes a package and install it inside the site-packages folder of your Python installation (be it your main/system wide Python installation, or one inside a virtual environment).
- Technically one can install a package with ```pip intall <path_to_source>```
- A useful option for dev is the editable mode ```pip install -e <path_to_source>``` ,  simlinks are installed and one can edit the code.
- you can pass the -e flag to make an editable install; in this case, changes to your files inside the project folder will automatically reflect in changes on your installed package in the site-packages folder.
- A better way is to make a source distribution tar file, see below.
- ```python setup.py sdist``` then will build a source archive. Means create a `dist` directory and put a tared project file there.
- The name of the tar file will be project_name-version.tar.gz and this is a source archive.
- Source archives can be distributed, but built distributions are better.
- Formerly built distributions were available in egg-format, now the prefered is the wheel format.
- Wheels are a pre-built distribution format that provides faster installation compared to Source Distributions (sdist), especially when a project contains compiled extensions.
- To generate a wheel distribution package, see [here](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)
- This is done with ```python3 setup.py sdist bdist_wheel```
- wheel is a built distribution, which I think is a compiled code for different platforms.

### Distributing and installing packages (PyPI, git, etc.)
- See https://packaging.python.org/tutorials/installing-packages/#requirements-for-installing-packages
- PyPI https://pypi.org Python Package Index - the usual and official python way.
    - https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives
    - register on PyPI
    - first use the Test PyPI repo, see above, and then you can use main PyPI
    - ```twine upload  dist/*```    
    - Then everybody can install the package with ```pip install [your-package]```
- Install from Git
    - See https://pip.pypa.io/en/latest/reference/pip_install/#vcs-support
    - ```pip install git+https://git.repo/some_pkg.git#egg=SomeProject ```
    - ```pip install git+https://git.repo/some_pkg.git@feature#egg=SomeProject  # from a branch```
    - ```pip install git+https://git.repo/some_pkg.git@v1.0#egg=SomeProject  # from a tag```
    - Often you will add a ```-e``` flag because the git stuff may be in development and you want to further develop a package. It will clone repo and make it editable.

### Distributing with conda/anaconda
- For a small project we can put conda recipe in the same project see [conda-recipe](conda-recipe)
```
conda install -y conda-build
conda install -y anaconda-client
anaconda login

conda-build -c conda-forge conda-recipe 
anaconda upload --force path_to_package #or toggle automatic upload with: conda config --set anaconda_upload True
conda convert --platform all path_to_package -o output/
find output/ -name 'seq_tools*' -exec anaconda upload --force {} \;
#Manually upload for OSX and Linux
```
- Installing  from Anaconda cloud

```
conda install -c intbio pypkg_example
```

### Tests
- Tests are an important concept in devloping reliable programs.
- Some libs in python exist to atutomate it, e.g. ```pytest``` or ```unittest```
- ```pytest``` looks convinient https://docs.pytest.org/en/latest/getting-started.html
- it runs files whcich start with test_*.py and functions in those files that are prefixed with test_*
- you can put tests in separate directory or not
```
tests/
|-- example
|   |-- test_example_01.py
|   |-- test_example_02.py
|   '-- test_example_03.py
|-- foobar
|   |-- test_foobar_01.py
|   |-- test_foobar_02.py
```

### Git Tags and GitHub releases
- https://help.github.com/en/github/administering-a-repository/creating-releases
- https://developer.github.com/v3/repos/releases/#create-a-release
- Creating tags from command line:
```
git tag <tagname>
#or
git tag -a v2.1.0 -m "xyz feature is released in this tag."
git push origin --tags
```
- If you tag a commit, it will appear on the releases GitHub page https://github.com/intbio/pypkg_example/releases
- Still to make it look like a normal release with some files attached you need to do it through the web interface.

### CI on git
- https://githubflow.github.io
- https://github.com/features/actions
- https://help.github.com/en/actions/automating-your-workflow-with-github-actions/about-continuous-integration
- https://help.github.com/en/actions/automating-your-workflow-with-github-actions/setting-up-continuous-integration-using-github-actions
- https://help.github.com/en/actions
- Through actions submenu we can add and edit workflows, these files will be put in .github/workflows subfolder.
- Workflows by default are exectuted on github servers.
- Workflows are triggered by actions - e.g. push, merge or release
- Badges can be generated by workflows and displayed elsewhere an example link is https://github.com/intbio/pypkg_example/workflows/Python%20package/badge.svg
- Badges default to master branch ![](https://github.com/intbio/pypkg_example/workflows/Testing/badge.svg)
- A branch name can be specified also, this is for ```feature1``` branch ![](https://github.com/intbio/pypkg_example/workflows/Testing/badge.svg?branch=feature1)
- GitHub Secretes see here https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets
- Autheticating with GITHUB_TOKEN https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token
- Important that one workflow cannot trigger another while using GITHUB_TOKEN.
- Note that jobs in workflows are executed in parallel - use steps for ordering actions.


### Docker
- See this tutorial https://docker-curriculum.com
