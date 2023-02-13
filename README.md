## About the Project

For those not familiar, Farkle is a dice game similar to Yahtzee where you roll dice and score points based on what you rolled. There is a pdf of the rules in the images file of the repository. This program is not a full Farkle game, but rather a simulation of just on turn of Farkle. It does not keep track of the points between rounds, except for the previous rounds points.

## Running the Project

There are two .py files: main.py and Points.py. In order to run the program, you will need pygame and random imported.

## How to Play

The program is pretty straight forward. There is a "roll" button that randomizes the dice. Then you can select any dice that you would like by clicking on them. If the program decides that it is legal for you to score the selected dice, the "keep" button will turn green and become clickable. Your selected dice will go to the bottom half of the screen and your points will go up. Now you can either select more dice to score or roll again. If you farkle, text will appear right below the upper dice that says "Farkle!". You can click done to start over; if you have farkled, there will be 0 in previous rounds points. If you did not Farkle, you will see however many points you scored in the prevoius rounds points.

