# Agent Pixel Art with Array
# 26 Feb 2023
# @JustinEducation

def on_on_chat():

    # teleport to player
    agent.teleport_to_player()
    
    # 2d array which contains pixel drawing 10x10.
    art_stack = [[BROWN_WOOL, GRAY_WOOL, GRAY_WOOL, BROWN_WOOL],
                [GRAY_WOOL, GRAY_WOOL, GRAY_WOOL, GRAY_WOOL],
                [GRAY_WOOL, BROWN_WOOL, BROWN_WOOL, BROWN_WOOL],
                [GREEN_WOOL, BROWN_WOOL, GREEN_WOOL, GREEN_WOOL]]

    player.say("Running code.")
    
    #loop through rows in array
    for row in art_stack:
        # for each item in a row
        agent.set_slot(1)
        for item in row:
            
            #move forward
            agent.move(FORWARD,1)
            #select the right resourcee in hot bar
            agent.set_item(item, 1, 1)
            # agent.set_item(item,1,1)
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
