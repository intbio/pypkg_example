#!/bin/bash

if [ -z "$1" ]
then
      echo "No arg specified - exiting"
      exit
else
      echo "Will create $1"
fi

if [[ -f "$1" ]]; then
    echo "$1 exists - exiting"
    exit
fi

if [[ -d "$1" ]]; then
    echo "$1 exists - exiting"
    exit
fi

TMPFILE=`mktemp`
curl -Lo $TMPFILE https://github.com/intbio/pypkg_example/archive/master.zip
unzip $TMPFILE
rm $TMPFILE
mv pypkg_example-master $1
cd $1
mv expkg $1
echo "0.0.1" > VERSION
sed -i.bak "s/pypkg_example/$1/" setup.py
sed -i.bak "s/An example python package/Package $1/" setup.py
sed -i.bak "s/Long description if needed ... /Package $1/" setup.py
sed -i.bak "s/\'foo/#\'foo/" setup.py
sed -i.bak "s/\'bar/#\'bar/" setup.py
rm setup.py.bak
sed -i.bak "s/expkg/$1/" MANIFEST.in
rm MANIFEST.in.bak

sed -i.bak "s/pypkg_example/$1/" conda-recipe/meta.yaml
sed -i.bak "s/expkg/$1/" conda-recipe/meta.yaml
rm conda-recipe/meta.yaml.bak 

sed -i.bak "s/pypkg_example/$1/" docker/Dockerfile
rm docker/Dockerfile.bak

sed -i.bak "s/pypkg_example/$1/" docker/README.md
rm docker/README.md.bak

sed -i.bak "s/pypkg_example/$1/" docker_test/README.md
rm docker_test/README.md.bak

sed -i.bak "s/pypkg_example/$1/" .github/actions/test/Dockerfile
rm .github/actions/test/Dockerfile.bak

echo "![](https://github.com/intbio/$1/workflows/Testing/badge.svg) - for master branch." > README.md
echo "This a new package $1" >> README.md

git init 
git add .
git commit -m "First commit"
hub create intbio/$1
git push -u origin HEAD

echo "Now go here https://github.com/intbio/$1/settings/secrets"
echo "Add secrets ANACONDA_USERNAME and ANACONDA_PASSWORD"
