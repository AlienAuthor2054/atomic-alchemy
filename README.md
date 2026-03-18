# ⚠️ Status: Archived / Completed ⚠️

This repository contains the original Python Tkinter version of Atomic Alchemy, created as a final project for Intro to Programming 2. Active development on this version has **ceased**.

I am planning to **rebuild and expand this project** using the Godot game engine.

![gameplay_clip](https://github.com/user-attachments/assets/ae02ef76-0b75-4a2d-bd29-ea723f32b3f1)

## Controls
- Drag atoms from the conveyor to the space below it- the Lab
- In the Lab, drag an atom or group of atoms to another to bond them
  - Look for yellow orbs around atoms, they represent how many more bonds can it form
- Left click a bond to upgrade to double and triple bonds; right click to downgrade/break bonds
- Drag molecules off-screen to declutter- no points lost on deleting molecules

## Overview
- The game spawns atoms of 4 elements (hydrogen, carbon, nitrogen, and oxygen) drifting on a conveyor belt.
- Using drag-and-drop, these can be placed below the conveyor into the Lab, an area for doing chemistry. There, they are bonded with each other to score points. Points can also be spent to undo bonds made between atoms. 
- The game is over when the 3-minute timer is up- score is determined from the point total on game over.

## Features
- Grid-based collision-aware atom/radical bond snapping
- Varied point values for different bonds
- Valence orbs on atoms representing sharable valence elections
- Intro sequence, music, SFX, textures, and options screen (by [@echoee](https://github.com/echoeee))
- Game over screen with local leaderboard (by [@Damguapo](https://github.com/Damguapo) and [@plainStar77](https://github.com/plainStar77))

Inspired by the game Crown Joules from IC2020 Games at https://interactivechemistry.org/CrownJoules6/
