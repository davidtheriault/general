#!/bin/zsh

# Written by David Theriault
# Run a compile check on all the perl files pending commit
# Useful as an additional step for code review.

FAIL=''
for file in `git diff --name-only  origin/master...HEAD`; do
    # just perl files
    if [[ $file =~ .*\.p[lm]$  ]]; then
        echo $file
        perl -cw $file
        # If failed to compile store file name.
        if [ $? -ne 0 ];then
            if [[ -z $FAIL  ]]; then
                FAIL="$FAIL, $file"
            else
                FAIL=$file
            fi
        fi
    fi
done

# print at end so all failures can easily be viewed,
# sometime perl prints out a lot of lines which could
# mask an earlier failure.
if [[ -z $FAIL  ]]; then
    echo "all files compile succssfully"
    exit 0
else
    echo "FAILED Compile: $FAIL"
    exit 1
fi
