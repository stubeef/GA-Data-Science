# Chipotle Command Line

### 1. `Head chipotle`
       `Tail chipotle`
*Columns refer to a dimension of the order, while the rows refer to a component in the order.*

### 2. `Tail chipotle`
*a. 1834*
### 3. `wc -l chipotle`
*a. 4623*
### 4. `grep -cri 'chicken' chipotle.tsv`
*a. 553*

`grep -cri 'steak' chipotle.tsv`

*a. 368*

*Chicken burritos are more popular.* 
### 5. `grep -cri 'chicken burrito'|grep -cri 'black beans'`
*a. 1345*
`grep -cri 'chicken burrito'|grep -cri 'pinto beans'`
*a. 582*

*Chicken burritos more often have black beans.*

### 6. `find -name *.tsv| wc -l`
*a. 2*
### 7. `find -name *.csv| wc -l`
*a. 26*
### 8. `grep -ri 'dictionary'| wc-l`
*a. 55*
