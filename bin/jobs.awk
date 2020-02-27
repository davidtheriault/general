#!/usr/bin/awk

# used like this:
# echo `jobs | awk -v blue=${BLUE} -v green=${GREEN} -v default=${DEFAULT} -f $HOME/dev/general/bin/jobs.awk`
# To format output of jobs for RPROMPT
# See .zshrc

{
    if(NR > 1 && NF >= 4) {
        printf "%s", green;
        printf "| ";
    }

    if($1 != " (pwd") {
        printf "%s", blue;
        for (i=4; i<=NF; i++) {
            printf "%s ", $i;
        }
    }
}
END { printf "%s", default; }
