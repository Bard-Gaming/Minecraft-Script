summon armor_stand ~ ~5 ~ {Invisible:1b, NoBasePlate:1b, NoGravity:1b, Tags:["mcs_get_block_temp"]}
$loot replace entity @e[type=armor_stand, limit=1, sort=nearest, tag=mcs_get_block_temp] armor.head mine $(x) $(y) $(z) netherite_pickaxe{Enchantments:[{id:"minecraft:silk_touch", lvl:1s}]}
$data modify storage $(storage) string.$(nbt) set from entity @e[type=minecraft:armor_stand, limit=1] ArmorItems[3].id
kill @e[type=armor_stand, tag=mcs_get_block_temp]