gameplay.set_game_mode(CREATIVE, mobs.target(NEAREST_PLAYER))
gameplay.set_weather(CLEAR)

def on_build():
    player.say("Building Course.")
    
    lava_pit_size = 10
    counterX = 0
    counterZ = 0
    
    agent.set_item(LAVA_BUCKET, 1, 1)
    agent.set_slot(1)
    agent.teleport_to_player()
    start_pos = agent.get_position()
    agent.teleport(start_pos, WEST)

    while counterX < lava_pit_size:
        while counterZ < lava_pit_size:
            agent.move(FORWARD, 1)
            agent.destroy(DOWN)
            agent.place(DOWN)
            counterZ +=1
        counterZ = 0
        if counterX % 2 == 0:
            agent.move(FORWARD, 1)
            agent.turn_left()
            agent.move(FORWARD, 1)
            agent.turn_left()
        else:
            agent.move(FORWARD,1)
            agent.turn_right()
            agent.move(FORWARD, 1)
            agent.turn_right()
        counterX +=1
    
    counterX = 0
    agent.teleport(start_pos, WEST)
    post_size = 1
    agent.set_slot(2)
    agent.set_item(GRASS, 64, 2)

    spaceZ = Math.random()* lava_pit_size
    if spaceZ > 10: spaceZ = 10

    while counterX < lava_pit_size:
        while counterZ < spaceZ:
            agent.move(FORWARD, 1)
            counterZ +=1
        agent.move(UP, 1)
        agent.place(DOWN)
        counterZ +=1
        agent.move(FORWARD, 1)
        agent.move(DOWN, 1)
        while counterZ < lava_pit_size:
            agent.move(FORWARD, 1)
            counterZ+=1
        counterZ = 0

        spaceZ = Math.random()* lava_pit_size
        if spaceZ > 10: spaceZ = 10

        if counterX % 2 == 0:
            agent.move(FORWARD, 1)
            agent.turn_left()
            agent.move(FORWARD, 1)
            agent.turn_left()
        else:
            agent.move(FORWARD,1)
            agent.turn_right()
            agent.move(FORWARD, 1)
            agent.turn_right()
        counterX += 1

player.on_chat("Build", on_build)
