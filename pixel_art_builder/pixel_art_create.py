# Agent Pixel Art with Array from Pizel Art Builder
# 14 March 2023
# @JustinEducation
# This file is to be used with array created by the pixel art builder, where the output is inserted into art_stack array.

def on_on_chat():

    # teleport to player
    agent.teleport_to_player()
    
    # 2d array which contains pixel drawing.
    art_stack = [[AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR],
    [AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR],
    [AIR, AIR, AIR, BLACK_WOOL, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, AIR, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, BLACK_WOOL, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, AIR, BLACK_WOOL, BLACK_WOOL, AIR, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR],
    [AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR],
    [AIR, AIR, AIR, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, BLACK_WOOL, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR],
    [AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR, AIR]]
    
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
            if agent.get_item_detail(1) == AIR:
                pass
            else:
                # place behind
                agent.place(BACK)
        #when row is built, move up
        agent.move(UP,1)
        # turn around
        agent.move(BACK, len(row))
        # move forward to be ready to build the newt line

# 'run' in chat runs code
player.on_chat("run", on_on_chat)
