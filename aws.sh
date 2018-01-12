#/bin/bash

sudo yum install git python36
git clone https://github.com/thelfensdrfer/trakt-helper.git
cd trakt-helper/
sudo pip-3.6 install -r requirements.txt
cd data/
wget http://files.grouplens.org/datasets/movielens/ml-20m.zip
unzip ml-20m.zip
mv ml-20m/*.csv .
rm -fr ml-20m*
cd ..
python36 src/Training.py
