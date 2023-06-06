
Implement player upgrades and organize save data for persistent ones

Some ideas:

* Persistents (stored on save):
  * Passives:
    * "Running Shoes" - Being able to turn around with an acceleration.
    * "I'll be back" -  Having lives.
    * "You gotta run!" - Move Speed increase.
    * "Tax avoidance" - Keep percentage of money when you die.
    * "There's no spoon" - Vulnerability time resistance.


* Run based (not stored on save):
  * Passives:
    *  "Nope!" - "Instant" turn (vx = -vx and vy = -vy on turn)
    *  "Giving 150%" - Accelerated movement (trade-off, you don't start moving instantly at top speed, but you get accelerated to 1.5x your current top speed)
    *  "Sabotage" - Randomly spit out "slow down" points that slow down enemies.
    *  "Big pill to swallow" - Enemies get slow-down when consuming small points and even slower when getting Powerups temporarily.

  * Actives:
    * "Boosters Engage! "- Ability to sprint briefly
    * "It's a trap!" - Able to leave a point that kills the enemy when collected.
    * "Decoy" - Able to leave a fake blinky (fixes sink.matrix somewhere and leave a sprite for x seconds)
    * "Bombtrack" - Leave a bomberman style bomb.
    * "Ghost walk" - Phase through walls. (1 or 2 tile wide limit)
    * "Phase Shift" - Press a button to mark a position, press it again to instantly teleport to it
    * "He's got a gun!" - Ability to shoot projectiles
    * "Haunt" - able to teleport "near" enemies. (save enemies location (i,j) every 1 to 2 seconds and use that to teleport.)
---
* Make it possible to die.

* Implement loss condition (all points collected)

* Game over game state.

* Make basic gameplay-loop work (When you finish a level you should go to
a "next one", some variable should store which level it is to store 
difficulty data.)

* Blinky should get "money" after each completed level. 
Money = ammount of points left on level after completion. 

* Transitions when level has been beaten (portal change)

---
Side stuff:

* Fix the badly formed mazes

* Overall innerworkings of a rogue-like

* (persistent progression and upgrades stored in a file)

* Game presentation stuff: 

* menu system 

* splash screen

* game over screen
