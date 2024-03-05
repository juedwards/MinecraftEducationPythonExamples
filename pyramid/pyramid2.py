# Pyramid Builder for MakeCode Python
# @JustinEducation
# 21 Feb 2023

# Set gameplay
gameplay.set_weather(CLEAR)
gameplay.time_set(DayTime.DAY)
gameplay.set_game_mode(CREATIVE, mobs.players_in_game_mode(CREATIVE))

# Set global variables
playerX = 0
playerY = 0
playerZ = 0

def on_chat():

    # Capture player position
    player_pos = player.position()
    playerX = player_pos.get_value(Axis.X)
    playerY = player_pos.get_value(Axis.Y)
    playerZ = player_pos.get_value(Axis.Z)
    
    # Randomize pyramid size
    base_size = randint(4, 40)

    # Calculate height of build based on base size
    height = (base_size // 2) + 1 if base_size % 2 == 0 else base_size // 2

    # Position the agent and give resources
    set_agent()

    # Build
    for index in range(height):
        for _ in range(4):
            for _ in range(base_size):
                if agent.detect(AgentDetection.BLOCK, FORWARD):
                    agent.destroy(FORWARD)
                agent.move(FORWARD, 1)
                agent.place(BACK)
            agent.turn(TurnDirection.LEFT)
        agent.move(UP, 1)
        agent.place(DOWN)
        agent.move(LEFT, 1)
        agent.move(FORWARD, 1)

        if agent.get_item_count(SANDSTONE) < 32:
            populate_agent()

        base_size -= 2

# Function to set position of agent and give resource
def set_agent():
    start_position = pos(playerX + 10, playerY, playerZ)
    agent.teleport(start_position, WEST)
    populate_agent()

# Function to give agent resources
def populate_agent():
    agent.set_slot(1)
    agent.drop_all(FORWARD)
    agent.set_item(SANDSTONE, 64, 1)

# Call pyramid build function
player.on_chat("pyramid", on_chat)
