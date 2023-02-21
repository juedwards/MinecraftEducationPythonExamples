# Pryamid Builder for MakeCode Python
# @JustinEducation
# 21 Feb 2023

# Set gameplay
gameplay.set_weather(CLEAR)
gameplay.time_set(DayTime.DAY)
gameplay.set_game_mode(CREATIVE, mobs.players_in_game_mode(CREATIVE))

#set global variables
playerX = 0
playerY = 0
playerZ = 0

def on_chat():

    #capture player position
    playerX = player.position().get_value(Axis.X)
    playerY = player.position().get_value(Axis.Y)
    playerZ = player.position().get_value(Axis.Y)
    
    #randomize pyramid size
    lower = 4
    upper = 40

    #set size of base
    rand_num = Math.random()
    base = rand_num * (upper-lower)

    #calculate height of build based on base size
    if base % 2 == 0:
        height = (base / 2) + 1
    else:
        height = base/2
   
    #set counters for build
    index = 0
    sides = 0

    #position the agent and give resources
    set_agent()

    #build
    while index < height:
        sides = 0
        while sides < 4:
            counter = 0
            
            while counter < base:
                if agent.detect(AgentDetection.BLOCK, FORWARD):
                    agent.destroy(FORWARD)
                agent.move(FORWARD, 1)
                agent.place(BACK)
                counter += 1

            agent.turn(TurnDirection.LEFT)
            sides += 1
        agent.move(UP, 1)
        agent.place(DOWN)
        agent.move(LEFT,1)
        agent.move(FORWARD,1)

        if agent.get_item_count(1) < 32:
            populate_agent()

        base -= 2
        index += 1

#function to set position of agent and give resource
def set_agent():
    start_position = pos(playerX+10, playerY, 0)
    agent.teleport(start_position, WEST)
    populate_agent()

#function to give agent resources
def populate_agent():
    agent.set_slot(1)
    agent.drop_all(FORWARD)
    agent.set_item(SANDSTONE, 64, 1)

#call pyramid build function
player.on_chat("pyramid", on_chat)
