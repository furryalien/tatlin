#!/usr/bin/env python3
"""Test script to debug the travels feature"""

# Simple test of the logic
class FakeMovement:
    def __init__(self, delta_e, flags=0):
        self.delta_e = delta_e
        self.flags = flags

# Simulate what happens in movement_color
travels_enabled = False  # This is what happens when checkbox is unchecked

test_movements = [
    FakeMovement(delta_e=0.02, flags=0),  # cutting (positive delta_e)
    FakeMovement(delta_e=0.0, flags=0),   # travel (zero delta_e)
    FakeMovement(delta_e=0.05, flags=16), # cutting (positive delta_e + FLAG_EXTRUDER_ON)
    FakeMovement(delta_e=0.0, flags=16),  # cutting? (FLAG_EXTRUDER_ON but no delta_e)
    FakeMovement(delta_e=-0.01, flags=0), # retraction (negative delta_e)
]

print("Testing movement_color logic:")
print(f"travels_enabled = {travels_enabled}\n")

for i, move in enumerate(test_movements):
    extruder_on = move.flags & 16 or move.delta_e > 0
    
    if extruder_on:
        color = "RED (visible)"
        move_type = "CUTTING"
    else:
        if travels_enabled:
            color = "GRAY (visible)"
            move_type = "TRAVEL"
        else:
            color = "TRANSPARENT (hidden)"
            move_type = "TRAVEL"
    
    print(f"Move {i}: delta_e={move.delta_e:6.2f}, flags={move.flags}, extruder_on={extruder_on} -> {move_type} -> {color}")
