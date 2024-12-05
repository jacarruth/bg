# bg
AI backgammon player

To play a game, run the file "play.py". Player types are chosen via the variables playerW and playerB (for White and Black, respectively) in the file "play.py".

## Available player types:

- Human:

  Moves are specified by user input of the form 1S, 1F, 2S, 2F,..., NS, NF. Here N is the number of moves to be made and iS, iF represent the initial position and final position of the checker to be moved with the ith move. To move a checker off the bar, one uses the string 'BAR' as initial position. To move a checker off the board, one uses the string 'OFF' as final position.

  For example, the input 'BAR', 3, 17, 22 moves one checker from the bar to position 3 and another checker from position 17 to 22 (provided this is a legal move).

- TDGammon:

    An implementation of G. Tesauro's first TDGammon player (see [here](https://proceedings.neurips.cc/paper/1991/file/68ce199ec2c5517597ce0a4d89620f55-Paper.pdf)). Neural net with one hidden layer, 50 nodes (parameters alpha=.1 and lambda=.7), and raw board state as input. Trained via 200,000 games of self-play.

- pubeval:

    Tesauro's proposed public benchmark player (see [here](https://www.bkgm.com/rgb/rgb.cgi?view+610)).

- Random:

    Random selection from list of all possible moves.
