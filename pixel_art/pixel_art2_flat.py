# Agent Pixel Art with Array
# 26 Feb 2023
# @JustinEducation

def on_on_chat():

    # teleport to player
    agent.teleport_to_player()
    
    # 2d array which contains pixel drawing 10x10.
    art_stack = [[3,3,8,3,3,3,8,3,8,3],
                 [8,3,3,8,3,3,3,8,3,3],
                 [3,8,3,4,3,3,4,3,3,8],
                 [8,3,3,4,4,4,4,3,8,3],
                 [3,8,3,4,4,4,4,8,3,8],
                 [8,3,3,8,4,4,8,8,3,3],
                 [8,3,4,4,3,8,4,4,8,3],
                 [3,8,4,4,8,3,4,4,3,8],
                 [8,3,3,8,3,3,3,8,3,3],
                 [3,3,8,3,3,3,8,3,8,3]]

    # loads color blocks with Agent
    agent.set_item(RED_CONCRETE,64,1)
    agent.set_item(BLUE_CONCRETE,64,2)
    agent.set_item(GREEN_CONCRETE,64,3)
    agent.set_item(BLACK_CONCRETE,64,4)
    agent.set_item(ORANGE_CONCRETE,64,5)
    agent.set_item(PURPLE_CONCRETE,64,6)
    agent.set_item(CYAN_CONCRETE,64,7)
    agent.set_item(LIME_CONCRETE,64,8)
    agent.set_item(PINK_CONCRETE,64,9)

    player.say("Running code.")
    
    # set agent facing north
    agent.teleport(pos(5, 0, 0), NORTH)
    
    #loop through rows in array

    current_row = 0

    for row in art_stack:
        # for each item in a row
        for item in row:
            #move forward
            agent.move(FORWARD,1)
            #select the right resource in hot bar
            agent.set_slot(item)
            # place behind
            agent.place(BACK)
        if current_row % 2 == 0:
            #when row is built, move right
            agent.turn_right()
            agent.move(FORWARD,1)
            # turn to face north
            agent.turn_right()
            agent.move(FORWARD, 1)
        else:
            #when row is built, move right
            agent.turn_left()
            agent.move(FORWARD,1)
            # turn to face north
            agent.turn_left()
            agent.move(FORWARD, 1)
        current_row +=1
        
    player.say("Done.")

# 'run' in chat runs code
player.on_chat("run", on_on_chat)
