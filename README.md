# Police Robot, Gr.12 Digital Electronics Project

This is a group project in class to restore an old bomb defusal robot frame that was donated to our school's tech department.
By restore, I mean we want to drive it around and maybe shoot nerf darts, not actually defuse bombs.

The group: Jessie (Me), Owen, Donika, Andrew.

All code by me, unless otherwise noted. Other group members are more focused on the electronics portion of the project.

## Project Overview
Our group is working with the empty metal frame of an old bomb defusal robot that was donated to the school's electronics department as a frame and motors to add the circuitry ourselves to.

We have made new h-bridges to power the various motors of the robot, and the brains of the robot is a Raspberry Pi 3b.
So far, I have made code that will allow us to control the robot from a Wii Remote using controls similar to playing Mario Kart on the Nintendo Wii. The code controls the directions of the motors using GPIO pins connected to the h-bridges.

I have also worked on setting up a camera server on the Pi in order for a camera feed from the Robot to be accessed from local computers. Not shown in the repository, I have made a script that helps switch the Raspberry Pi from being connected to Wifi to acting as an Access Point, since the school wifi does not allow for port connections. The camera server code is, for the moment, a slightly modified version of [Patrick Fuller's Camp Webserver Code](https://github.com/patrickfuller/camp), though this is just temporary and I am hoping to create my own code in the near future.


![Robot Icon](https://raw.githubusercontent.com/greenhoodie/police-robot/master/Icon.png)
>Lovely paint style arwork by Donika

## Please note: 
This repository is merely for my own organizational purposes and to get used to using Github. The code is not meant to work for any general application, and all issues and pull requests made by others will be ignored.
