# Minecraft Education Python Examples
Examples of Minecraft Education Python Scripts

This site will build into a collection of python scripts for building objects in Minecraft Education, using MakeCode python IDE.

The scripts will build mainly single objects and can be combined together.

HOUSE

This is a Python code for a Minecraft game that builds a house with walls and roof. The gameplay.set_weather(CLEAR) and gameplay.time_set(DayTime.DAY) functions set the weather and time of day in the game. The on_on_chat() function is called when the player enters the chat command "house".

The size, walls, and height variables determine the dimensions of the house. The start_position variable stores the position of the player before the house is built. The agent.set_slot(1) and agent.set_item(STONE,64,1) functions set the agent's inventory slot to hold 64 units of stone for building walls.

The while loop builds the walls of the house by placing blocks and moving forward and turning left. The agent.move(UP,1) and agent.place(DOWN) functions move the agent up one block and place a block underneath to create a solid floor.

The base variable is used to determine the size of the roof. The index and sides variables are used to keep track of the number of roof sections and sides built. The agent.set_slot(2) and agent.set_item(OAK_WOOD_STAIRS,64,2) functions set the agent's inventory slot to hold 64 units of oak stairs for building the roof.

The while loop builds the roof by placing blocks, turning left and right, and moving forward and backward. The agent.move(UP, 1) and agent.place(DOWN) functions move the agent up one block and place a block underneath to create a solid roof.

Overall, this code can be used in Minecraft to build a simple house with walls and a roof.

PYRAMID

Creates a sandstone pyramid of random size.

STAIRS

Creates stairs down from a high point.
