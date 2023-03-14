# Pixel Art Created with Array
# 14 March 2023
# @JustinEducation
# This is similar to the pizel_art_create.py, uses builder instead of agent, therefore is much quicker in building file.
# The array in this code will make a PI mathematical symbol, 16x16, as an example.

def on_on_chat():

    # teleport to player
    builder.teleport_to(pos(10,0,0))
    
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
        for item in row:
            
            #move forward
            builder.move(FORWARD, 1)
            #select the right resourcee in hot bar
            if item == AIR:
                pass
            else:
                # place behind
                builder.place(item)
        #when row is built, move up
        builder.move(UP,1)
        # turn around
        builder.move(BACK, len(row))
        # move forward to be ready to build the newt line

# 'run' in chat runs code
player.on_chat("run", on_on_chat)
