#!/bin/bash
# modified from https://stackoverflow.com/a/11099014

DATAFILE=${1}
COLUMNFILE=${2}

awk -F '\t' -v colsFile="$COLUMNFILE" '
   BEGIN {
     j=1
     while ((getline < colsFile) > 0) {
        col[j++] = $1
     }
     n=j-1;
     close(colsFile)
     for (i=1; i<=n; i++) s[col[i]]=i
   }
   NR==1 { sep=""
     for (f=1; f<=NF; f++)
       if ($f in s) {
         c[s[$f]]=f
         printf("%c%s",sep,$c[s[$f]])
         sep=FS
       }
     print ""
     next
   }
   { sep=""
     for (f=1; f<=n; f++) {
       printf("%c%s",sep,$c[f])
       sep=FS
     }
     print ""
   }
' "$DATAFILE"
