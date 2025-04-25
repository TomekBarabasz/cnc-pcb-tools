# cnc tools
## cutoff
yaml file format:
```
geometry:
  origin: 0,0
  width: 10
  height: 20
  corner-radius: 10
cut:
  depth: 1.8
  feed: 100
  zfeed: 30
  layer: 0.5
bridge:
  size: 4
  depth: 1.5
  density: 50 # one bridge to be placed per 'density' number of units 
tool:
  diameter: 1.5
  shape: circle # if shape is 'v' specify blade angle
  zmoving: 5 # z height when moving
```
## APAR
this wiil be auto-place-and-route module with some cool
stuff 
