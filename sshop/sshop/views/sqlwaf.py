import re
def checkwaf(str):
    p=r"select|insert|update|delete|union|into|as"
    p+="|'|\"|\*|\.|=|\(|\)| |-|\x00|#"
    #p+="|'|\"|\*|\.|=|(|)| |-|\x00|#"
    p+="|and|or"
    p+="|load_file|outfile|dumpfile|bin|sub|hex"
    pattern=re.compile(p,re.I)
    matcher=re.search(pattern,str)
    if matcher:
        return 1
    else:
        return 0
def checkuser(str):
    i=0
    for i in range(len(str)):
        if((ord(str[i])>=48 and ord(str[i])<=57)or(ord(str[i])>=65 and ord(str[i])<=90)or(ord(str[i])>=97 and ord(str[i])<=122)or ord(str[i])==95):
            return 0
        else:
            return 1

def checkpass(str):
    i=0
    for i in range(len(str)):
        if(len(str)>=6 and( (ord(str[i])>=48 and ord(str[i])<=57)or(ord(str[i])>=65 and ord(str[i])<=90)or(ord(str[i])>=97 and ord(str[i])<=122)or ord(str[i])==95)):
            return 0
        else:
            return 1