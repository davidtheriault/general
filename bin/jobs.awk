#!/usr/bin/awk

# used like this:
# echo `jobs | awk -v blue=${BLUE} -v reset=${RESET} -f $HOME/dev/general/bin/jobs.awk
# To format output of jobs for RPROMPT
# See .zshrc

{
   # printf $0 "\n"
    if(NR > 1 && NF >= 4) {
        printf reset;
        printf "| ";
    }

    if($1 != " (pwd") {
        printf blue;
        for (i=4; i<=NF; i++) {
            #printf " {line %d, col:%dof%d:%s}", NR, i, NF, $i;
            printf "%s ", $i;
        }
        printf reset;
    }
}
END { printf "\n"; }
