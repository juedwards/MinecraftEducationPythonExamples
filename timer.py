# Time World
# 28 Feb 2023
# @JustinEducation


# sets some global variables
agent_location = agent.get_position()
sec_clock = 0
game_loop = False
agent_location2: Position = None
counterX = 0
counterY = 0
displayX = 0
displayY = 0

def on_on_chat():
    global displayY, displayX, counterX, counterY, agent_location2
    
    #teleport agent to a location to build display.
    agent.teleport(pos(10, 0, 0), WEST)
    #load resources
    agent.set_item(REDSTONE_LAMP, 64, 1)
    agent.set_slot(1)
    #set size of display
    displayY = 5
    displayX = 5

    # agent builds display
    while counterY < displayY:
        while counterX < displayX:
            agent.move(FORWARD, 1)
            agent.place(BACK)
            counterX += 1
        counterX = 0
        agent.move(UP, 1)
        agent.turn_right()
        agent.turn_right()
        agent.move(FORWARD, 1)
        counterY += 1
    
    agent.move(RIGHT, 1)
    agent.move(DOWN, displayY)
    agent.move(FORWARD, displayX-1)
    agent.destroy(DOWN)
    agent.move(DOWN, 1)

    # agent location is set and used in next function to add redstone.
    agent_location2 = agent.get_position()

    on_on_chat2()

def on_on_chat2():
    global game_loop, sec_clock
    player.say("Timer Started.")
    
    # holds open the while loop, so that the numbers keep cycling.
    game_loop = True
    while game_loop:
        # wait 1 second
        loops.pause(1000)
        # clears the display of redstone blocks
        blocks.print("", AIR, agent_location2, WEST)
        sec_clock += 1
        # if the number is larger than 9 return to 0
        if sec_clock > 9:
            sec_clock = 0

        #print on screen the time
        player.say("Seconds: " + str(sec_clock))

        #find the right number to display and then draw the redstone behind the redstone lamps for that number.            
        if sec_clock == 1:
            blocks.print("1", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 2:
            blocks.print("2", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 3:
            blocks.print("3", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 4:
            blocks.print("4", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 5:
            blocks.print("5", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 6:
            blocks.print("6", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 7:
            blocks.print("7", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 8:
            blocks.print("8", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 9:
            blocks.print("9", REDSTONE_BLOCK, agent_location2, WEST)
        elif sec_clock == 0:
            blocks.print("0", REDSTONE_BLOCK, agent_location2, WEST)

player.on_chat("run", on_on_chat)




