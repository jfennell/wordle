## What is this?
Some scripts & analyses around the game Wordle.

## How does it work?
In `wordle.py` there is a `Solver` class that gets initialized with a vocabulary.

The solver iteratively:
- Computes a letter frequency count through the vocabulary
- Computes a score for each `word` that is the _sum_ of the letter _frequencies_ for each _unique_ letter in the `word`
- Queries "Wordle" to receive an answer about which letters are not in the word, in the word in the wrong position or in the word in the right position
- Removes all words from the vocabulary that don't match the positional info received
- Repeats until all letters match

## What can I do with this?
`python interactive.py` will give you an interactive prompt that you can use to assist with solving Wordle puzzles. The default vocabulary is contained in `words_alpha.txt` and seems to be a large superset of the dictionary [Wordle](https://www.powerlanguage.co.uk/wordle/) uses, so you need to guide the solver a bit to find a word that will be accepted. (If you know of a dictionary resource that better matches what Wordle actually uses please let me know!)

`python solve_all.py` will run for a while (~15min) and leave `solve_path_out.json` in the working directory. This documents the series of "guesses" that the fully automatic solver makes to solve the puzzle using every single vocabulary word in turn as the puzzle seed. `python analysis.py` will spit out a basic analysis of these solves.

## What did you learn about Wordle in this process?
 - Turns out words that are part of a cluster that differ by a single letter in the same position are hard to solve.
 - Wordle's responses give you a lot of data. This basic heuristic solves > 90% of seeds within the required number of moves. That likely goes up quickly if you have a better-matching dictionary (based on my interactive play)

## Thanks / Resources
- https://github.com/dwyl/english-words is the source of the word dictionary
- You! Thanks for reading this far. I have no idea how you found the page, but I hope you have some fun with this.
<<<<<<< Updated upstream
=======


## TODO
- [ ] Update the vocab options to include one that is just the Wordle word list
- [ ] Play with a new solver that better bounds the maximum "depth" of solve (inspired by reading wordle-bot summaries)
>>>>>>> Stashed changes
