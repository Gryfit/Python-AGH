10 INPUT x
20 INPUT y
25 IF x==0 THEN GOTO 70
30 IF y==0 THEN GOTO 60
33 LET r=y
35 LET y=x%y
38 LET x=r
50 IF y!=0 THEN GOTO 33
60 PRINT x
70 PRINT y
