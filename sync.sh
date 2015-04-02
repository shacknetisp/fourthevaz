if [[ $@ == **upload** ]]
then
git add --all -v .
git commit
git push
git push origin --tags
fi
find . -name "*.pyc" -exec rm -rf {} \;
git pull
