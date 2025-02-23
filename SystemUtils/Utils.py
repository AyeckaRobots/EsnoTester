from SystemUtils.StaticVars import s2x_starting_index, all_pls_simplified
import time


def update_pls_list(standard):
    pls = s2x_starting_index
    while pls not in all_pls_simplified and pls <= 300:
        pls += 1
    if standard == 's2':
        return all_pls_simplified[:all_pls_simplified.index(pls)]
    elif standard == 's2x':
        return all_pls_simplified[all_pls_simplified.index(pls):]
    elif standard == '':
        return all_pls_simplified

def load(t):
    """A function that creates a loading animation on the console while counting down
    acts as time.sleep() for t larger than 0.2s

    Args:
        t (int): time until function ends
    """
    index = 0
    time_elapsed = 0
    sign = ['/', '-', '\\', '|']
    while time_elapsed < t:
        print(f"Loading... [{sign[index]}]", end="\r")
        time.sleep(0.2)
        time_elapsed += 0.2
        index = (index + 1) % 4