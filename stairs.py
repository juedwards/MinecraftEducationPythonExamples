# Stairs Builder for MakeCode Python
# Creates  staircase into a Mineshaft
# @JustinEducation
# 23 Feb 2023

# Set gameplay
gameplay.set_weather(CLEAR)
gameplay.time_set(DayTime.DAY)

def on_on_chat():
    #populate agent with resources
    resource_add()
    agent.set_slot(1)
    #Teleport to player and face same direction.
    agent.teleport(player.position(),positions.to_compass_direction(player.get_orientation()))
    #record starting position and orientation
    agent_start_pos = agent.get_position()
    agent_start_orientation = agent.get_orientation()
    #find depth and distance
    depth_count = detect_mineshaft()
    #return to start
    agent.teleport(agent_start_pos, positions.to_compass_direction(agent_start_orientation))
    loops.pause(50)
    #build stairs
    build_stairs(depth_count)

#function to add resource
def resource_add():
    agent.set_item(STONE_BRICKS, 64, 1)
    agent.set_item(TORCH,64,2)
    agent.set_item(STONE_BRICK_STAIRS, 64, 3)
    agent.set_item(POWERED_RAIL, 64, 4)
    agent.set_item(RAIL, 64, 5)
    agent.set_item(REDSTONE_LAMP, 64, 6)

#function to detect distance
def detect_mineshaft():
    agent.move(FORWARD, 1)
    depth_count = 0
    while not agent.detect(AgentDetection.BLOCK, DOWN):
        agent.move(DOWN,1)
        agent.move(FORWARD,1)
        depth_count += 1
    player.say("The initial depth is: " + depth_count)
    return depth_count

# function to build stairs
def build_stairs(depth: number):
    agent.set_slot(3)
    agent.move(FORWARD, 1)
    count = 0
    agent.turn_left()
    agent.turn_left()
    while count < depth:
        if agent.detect(AgentDetection.BLOCK, DOWN):
            agent.destroy(DOWN)
        agent.move(DOWN, 1)    
        agent.move(BACK, 1)
        agent.place(FORWARD)
        count += 1

player.on_chat("run", on_on_chat)
