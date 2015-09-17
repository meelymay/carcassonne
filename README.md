carcassonne
===========

For now: $ python game.py

a nifty game and tile calculator for the game Carcassonne

Game
    ''' Keeps track of whose turn, prompts players, checks input, etc. '''
    # members
    players
    board

Board
    #members
    deck
    grid
    territories
    #methods
    place_tile(tile, coordinate)
        
    place_meeple(coordinate, section)
    score()
        for territy in territories:
            territory.score()
    
Deck
    tiles
    
Player
    meeples
    score
    
Tile
    meeple
    n,s,e,w,nne,ene,sse,ese,nnw,wnw,ssw,wsw
    
      nnw n nne  
     wnw  nc ene
     w wc c ec e
     wsw  es ese
      ssw s sse
      
Territory
    ''' Can be Road, Castle, Cloister, Farm '''
    meeples
    tiles
    #methods
    score
        ''' returns (meeple, score)  '''
    
    
