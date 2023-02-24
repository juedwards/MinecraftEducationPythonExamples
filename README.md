# Minecraft Education Python Examples
Examples of Minecraft Education Python Scripts

This repository a collection of python scripts for building objects in [Minecraft Education](https://education.minecraft.net/en-us), using MakeCode python IDE. There is a [reference guide](https://minecraft.makecode.com/reference) for MakeCode in Minecraft and a range of [example](https://minecraft.makecode.com/projects) that you might want to try.

## HOUSE

This is a Python code for a [Minecraft Education](https://education.minecraft.net/en-us) game  that builds a house with walls and roof. The on_on_chat() function is called when the player enters the chat command "house".

The size, walls, and height variables determine the dimensions of the house. The start_position variable stores the position of the player before the house is built. The agent.set_slot(1) and agent.set_item(STONE,64,1) functions set the agent's inventory slot to hold 64 units of stone for building walls.

The while loop builds the walls of the house by placing blocks and moving forward and turning left. The agent.move(UP,1) and agent.place(DOWN) functions move the agent up one block and place a block underneath to create a solid floor.

The base variable is used to determine the size of the roof. The index and sides variables are used to keep track of the number of roof sections and sides built. The agent.set_slot(2) and agent.set_item(OAK_WOOD_STAIRS,64,2) functions set the agent's inventory slot to hold 64 units of oak stairs for building the roof.

The while loop builds the roof by placing blocks, turning left and right, and moving forward and backward. The agent.move(UP, 1) and agent.place(DOWN) functions move the agent up one block and place a block underneath to create a solid roof.

## PYRAMID

Creates a sandstone pyramid of random size.

## STAIRS

Creates stairs down from a high point.
