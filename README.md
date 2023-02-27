# Minecraft Education Python Examples
Examples of Minecraft Education Python Scripts

This repository a collection of python scripts for building objects in [Minecraft Education](https://education.minecraft.net/en-us), using MakeCode python IDE. There is a MakeCode [reference guide](https://minecraft.makecode.com/reference) for Minecraft and a range of [examples](https://minecraft.makecode.com/projects) provided by MakeCode that you might want to try.

## Pixel Art with Arrays

This is a Python script for Minecraft Education that draws a pixel art using the Agent's abilities. The pixel art is represented as a 2D array of numbers, where each number represents a color block. The script loads the appropriate color blocks into the Agent's inventory and then uses a loop to move the Agent and place the blocks in the correct pattern to draw the pixel art.

The script begins by teleporting the Agent to the player's location, so that the pixel art will be drawn near the player. It then defines the pixel art as a 2D array called art_stack. Each row in the array represents a row in the pixel art, and each item in a row represents a block in that row.

Next, the script loads the color blocks into the Agent's inventory using the set_item function. Each color block is assigned a number from 1 to 9, which corresponds to the numbers in the art_stack array.

The script then enters a loop that iterates over each row in the art_stack array. For each row, it moves the Agent forward and selects the appropriate color block using the set_slot function. It then places the block behind the Agent using the place function. After all blocks in the row have been placed, the Agent moves up one block, turns around, and moves forward one block to prepare for the next row.

Finally, the script defines an event handler that will run the code when the player types "run" in the chat.

Note that the script assumes that the Agent has enough blocks of each color in its inventory to draw the entire pixel art. If the Agent runs out of blocks, it will stop drawing and the pixel art may be incomplete.

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
