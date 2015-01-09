if [[ $@ == **upload** ]]
then
git add --all -v .
git commit
git push
fi
find . -name "*.pyc" -exec rm -rf {} \;
git pull
