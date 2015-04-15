if [[ $@ == **upload** ]]
then
#( find . -name '*' -not -path "./.git/*" -not -type d -not -path "./userdata/*" -print0 | xargs -0 cat ) | wc -l > linecount
git add --all -v .
git commit
git push
git push origin --tags
fi
find . -name "*.pyc" -exec rm -rf {} \;
git pull
