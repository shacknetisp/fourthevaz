if [[ $@ == **upload** ]]
then
git add --all -v .
git commit
git push
fi
git pull
