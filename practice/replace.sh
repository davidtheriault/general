# Perl Search and Replace, goes through files from find and replaces all occurances of PUPPY with NEW:
# perl -i tells it to make the changes to the file in place, could also use the -i.bak option which would leave the orginal with a .bak extention
perl -i -pe 's/OLD/NEW/g' filename
# -p option tells perl to run the code in -e for each line in the passed in file, assigning that line as $_
find -xtype f -name \* -a \! -path \*/.svn\* -a \! -path \*/.cvs\* | xargs  perl -p -e 's/PUPPY/NEW/g'
