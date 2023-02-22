# House Builder for MakeCode Python
# @JustinEducation
# 22 Feb 2023

# Set gameplay
gameplay.set_weather(CLEAR)
gameplay.time_set(DayTime.DAY)

def on_on_chat():
    
    size = 4
    walls = 4
    height = 2

    agent.teleport_to_player()
    start_position = agent.get_position()
    
    agent.set_slot(1)
    agent.set_item(STONE,64,1)

    counter_height = 0
    while counter_height < height:
        counter_walls = 0
        while counter_walls < walls:
            counter_size = 0
            while counter_size < size:
                if agent.detect(AgentDetection.BLOCK, FORWARD):
                    agent.destroy(FORWARD)
                agent.move(FORWARD, 1)
                agent.place(BACK)
                counter_size +=1
            agent.turn(TurnDirection.LEFT)
            counter_walls +=1
        agent.move(UP,1)
        agent.place(DOWN)
        counter_height +=1
    
    agent.move(BACK, 1)
    agent.move(RIGHT, 1)

    base = size+2
    if base % 2 == 0:
        height = (base / 2) + 1
    else:
        height = base/2
    
    #set counters for build
    index = 0
    sides = 0

    agent.set_slot(2)
    agent.set_item(OAK_WOOD_STAIRS,64,2)

    #build roof
    while index < height:
        sides = 0
        while sides < 4:
            counter = 0
                
            while counter < base:
                if agent.detect(AgentDetection.BLOCK, FORWARD):
                    agent.destroy(FORWARD)
                agent.move(RIGHT,1)
                agent.turn_left()
                agent.place(FORWARD)
                agent.turn_right()
                agent.move(FORWARD, 1)
                agent.move(LEFT,1)  
                counter += 1

            agent.turn(TurnDirection.LEFT)
            sides += 1
        
        agent.move(UP, 1)
        agent.place(DOWN)
        agent.move(LEFT,1)
        agent.move(FORWARD,1)    

        base -= 2
        index += 1

    
player.on_chat("house", on_on_chat)
