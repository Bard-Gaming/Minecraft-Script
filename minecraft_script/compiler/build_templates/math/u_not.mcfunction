# !bool = (bool + 1) % 2

scoreboard players operation .out mcs_math = .a mcs_math
scoreboard players set .b mcs_math 1
scoreboard players operation .out mcs_math += .b mcs_math
scoreboard players set .b mcs_math 2
scoreboard players operation .out mcs_math %= .b mcs_math