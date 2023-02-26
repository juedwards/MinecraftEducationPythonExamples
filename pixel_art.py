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
    
    #loop through rows in array
    for row in art_stack:
        # for each item in a row
        for item in row:
            #move forward
            agent.move(FORWARD,1)
            #select the right resourcee in hot bar
            agent.set_slot(item)
            # place behind
            agent.place(BACK)
        #when row is built, move up
        agent.move(UP,1)
        # turn around
        agent.turn_left()
        agent.turn_left()
        # move forward to be ready to build the newt line
        agent.move(FORWARD,1)

# 'run' in chat runs code
player.on_chat("run", on_on_chat)
