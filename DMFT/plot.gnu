set nokey
set xrange [-5: 5]
#set yrange [ 0.03 :  0.08]
#set arrow from  0.32901,  -1.19843 to  0.32901,   8.26311 nohead
#set arrow from  1.01403,  -1.19843 to  1.01403,   8.26311 nohead
#set xtics (" G "  0.00000," X "  0.32901," M "  1.01403," G "  1.67523)
set arrow from 0,0 to 0,1 nohead
 plot "Sig1.out" u ($1):($2) with lines
 replot
