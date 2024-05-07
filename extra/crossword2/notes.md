### general issues
- [x] should grid-size be determined by the word-list?  eg: start with size = longest word + x * len(wordlist): currently starting grid-size corresponds to the largest word + 2

### crossword constraints
- [x] there should be a max word count (currently 25)
- [ ] should there be a max length for words? if so, which? (currently 40) - 40 is the max-size for grid. if a word is larger than 40 chars the generator will never stop running.

###  word placement constraintss
- [x] indexes for rows and columns need to be within grid range: start[row,col] cannot be smaller than 0 and end[row,col] cannot be >= len(grid)
- [x] no conflict within a same square: a new value cannot be assigned to cells that are not None
- [x] no end-to-end: each word should have an empty square at the start and end cells according to direction
- [x] no side-by-side: once two words intersect, the diagonal tiles of the intersection are blocked to avoid words clustering of words.

### optimizing
- [x] evaluate words before starting generator: if a word has no chars in common with the other words, it should not be placed. 
- [ ] the while clause in iterative_placement could be better. Now it will run for twice the initial length of words or until words is empty
- [ ] for each char in word, builder will iterate and find all possible intersections for that char and check if they are a valid placement, if so, will randomly choose one of the valid placements

### scoring
I need to decide if i am goiing
- I think ideally there would be an eval algorithm that can be called while words are being placed in the grid: 
    - maybe look for all possible placement of words (instead of first match): then check the evaluation of each resulting partial grid and keep the best score.
- [?] the more balanced between horizontal and vertical words the better ?
- [?] two or more words that are side by side in the same direction is not great - the longer they are side by side, the worst it gets.Ideally only intentional intersections (intersections of words in different directions) would have letters on all sides.
- width, height balance: a puzzle with a more balanced width height ratio is better
- less empty spaces: once trimmed, a puzzle with less empty spacess is better than a puzzle with a lot of empty spaces.
- all words in: not using all the words in a word-list is a serious offence

## sources
https://www.baeldung.com/cs/generate-crossword-puzzle
