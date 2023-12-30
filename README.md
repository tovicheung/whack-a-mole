# Whack a mole (on steroids)
This is the classic whack a mole game ... but on steroids!
I made this for my CS50 final project.

## Play the game
0. Install `pygame` (and python) if you haven't already
```
pip install pygame
```

1. Clone the repo
```
git clone https://github.com/tovicheung/whack-a-mole
```

2. cd into the directory and run `main.py`
```
cd whack-a-mole
python3 main.py
```

## How to play?
You have 30 seconds to WHACK the mischievous moles and gain points. For each mole you successfully WHACK you gain a point. However, these cunning moles will disappear after 3 seconds after appearing so you gotta be quick!
Move your mouse and click on a mole to WHACK it!

## Power-Ups
Just clicking on moles is boring though, that's why there's an exciting twist: power-ups. As you are focused on whacking the moles, keep an eye out for power-ups. You can click on power-ups to activate them.

Power-ups will help you with the game and get more points (and are a little silly lol). Power-ups spawn every 2-5 seconds. However, theys only exists for 3 seconds before disappearing, so same with the moles -- you gotta be quick!

There are 3 types of power-ups:
#### Hourglass
The hourglass power-up gives you an extra 5 seconds. This could be a game-changer when there is extremely little time left!
#### Fox
Clicking on the fox power-up will summon 5 foxes that run across the screen to eat the moles and get more points.
#### Wind
Clicking on the wind power-up will summon a hurricane that follows the cursor for 3 seconds. The hurricane will blow away the moles and get more points for you. It will do its thing on its own, you don't need to click, just move the cursor around!
#### Graphics
The power-ups all have their own effects and graphics because it's cool i guess

## Screenshots
A fox power-up spawned
![A fox power-up spawned](screenshots/powerup_spawned.png)
The fox power-up in action, 5 foxes runnning across the screen eating moles
![The fox power-up in action, 5 foxes runnning across the screen eating moles](screenshots/foxes.png)
The wind power-up in action, destroying moles. (Each of those blue crosses was once a mole!)
![The wind power-up in action, destroying moles. (Each of those blue crosses was once a mole!)](screenshots/wind.png)

## Software / tools used
(this part exists because of the 2500 character limit)
- Python (version 3.12)
- pygame (version 2.5.2)
- VSCode
- https://www.remove.bg/ to remove png backgrounds
- https://ezgif.com/split to split gif into png frames
