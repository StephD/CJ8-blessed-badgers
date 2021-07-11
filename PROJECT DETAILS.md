# Here I write what is the game concept

## In-TUI-tion

In-tui-tion is a linear game that will make the player make action base of his intuition.
A pixel wake up in a box and need to find his way into the maze by using is intuition, look item to move forward into the game. All of this to be able to Escape the Box with your in-TUI-tion and also make you solve some puzzle :-D

### Intuition example and definition
Intuition : Direct knowledge without need to think, immediate knowledge, quick and ready insight
We need to find thing to do that will be obvious for the player to find the solution. Like, there is a locked door and a stone. My intuition tell me that the key should be under the stone OR you need a jacket because it's too cold. My intuition tell me that the clothe store might sell one.

## Start the game

First, we arrive in a start screen. This screen include a menu, team info, version

### Menu :

1. Start the game
2. Load last game (From saved game file. Only one available)
3. Tutorial
4. Quit

### Tutorial

The tutorial is a basic version of the game with explaination of how to play. It will allow us to build the basic interactions to have something running. After what we can extend this to the game version

During the tutorial, there is just a pixel appear in the center of a room. Just a message say "Welcome to the tutorial, we will have to find a way to get out now".
The player move inside the square freely. After 10 movements, a message say
"Ho there here is a door :-)" and a door appear on the screen on the top
The player should go to the door.
When the game detect the player close to the door, the message say "The door is lock, where is the key"?
After 10 movements, a pot with flower appear and the game say "Oh, here a pot with a flower, weird no?"
The player should go to the pot and when the game detect that you are close.
"Hey, you just find a key. I wonder what it can be used to"
The intuition of the player should tell him that the key open the door.. :-D
The player go to the door and message say "The key open the door". The door change and it's open.
The player move forward and go out.
The game detect the player go throught a door
In the tutorial, it's stop here and display message "Well done, you get out of here, wanna try the real challenger?"
In the game, it will load the next room.

### Start the game
### Story (STORY TELLER)

First, need to show story displayed on the screen instead of the player. The message will be display in the bottom, top bar? or Pop-up message. I like the message in the bottom as the player don't have to make action with them and it doesn't "block" the game

### Game itself (LEVEL DESIGN)

It will display the game screen. Here is an example. What ever border we can make ahah

```
.____________________.
||------°°°°-----|   |
||               |   |
||               |   |
||       @       |   |
||               |   |
||---------------|   |
|________________|___|
```

Here is example with color:

https://dxtz6bzwq9sxx.cloudfront.net/demo_3rdparty_githeat.gif
https://github.com/AmmsA/Githeat

The side bar is for displaying the item, of what the player own.
The bottom bar car be for other kind of informations time the time left

### Movements & actions (USER INTERACTION)

With the keyboard, the player with make action into the game. Arrow keys are use to move. 'a' can be for making an action. 'd' for drop an item. 'u' for using an item (potion to get heal?), 'q' for quit.


### Interactions with the environment (GAME INTERACTION)

When the player move, there is a detect of the elements.

Elements can be door, other character, item, look, coin, frame, puzzle, ....

When the player arrive next to something, a message is display and propose the player to interact ('a' for action).
If it's a puzzle, may be a pop-up message with the question and input the answer.

#### Changing the room

When the player pass a door, the room need to change. The room design need to be loaded and display in the screen.

### Database (DATABASE)

When the player interact with something, there is an player object that will be updated with all the structure of where the player is in the game. I don't know yet the structure but can be :
```
{
    "room":{
        '1':{
            is_door_unlock:True,
            is_key_is found: True,
            is_secret_door_found: False,
        },
        '2':{
            ...
        }
    }
    "items":{"keys_remaining":1, 'lifes_left':2, ..}
}
```
Need to design it :-)

### Saving the game (FILE MANAGEMENT)

All the user data will be saved into a file and read if the player load the game.

Can use 'pandas' to read into a CSV and associate everything?

### Level generation (FILE MANAGEMENT)

All the actions, door interaction need to be read somewhere. Like what action is need to make this appear. Like the solution of the questions.
Or what door bring to what room. The game need to read somewhere the passing the door 4 in the room 3 will bring to the room 6, and passing the door 4 in the room 6 will bring the to room 3 !

+ Instead of hardcode the room layout. This can be setup into a file and we just need to edit the file to edit a level.
Need to be a 2D dataset with every rows and lines. Not yet sure how to deal with that
