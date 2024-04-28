### placement constraints
- [x] indexed for rows and columns need to be within grid range: start(row,col) cannot be smaller than 0 and end[row,col] cannot be >= len(grid)
- [x] no conflict within a same square: a new value cannot be assigned to cells that are not None
- [ ] no end-to-end: each word should have an empty square at the start and end cells according to direction
- [ ] no side-by-side: two words in the same direction should not be next to each other. there should always be an empty line in between them 

### optimizing


### scoring
- width, height balance: a puzzle with a more balanced width height ratio is better
- less empty spaces: once trimmed, a puzzle with less empty spacess is better than a puzzle with a lot of empty spaces.
- all words in: not using all the words in a word-list is a serious offence
