# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import math
import builtins

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = math.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(measurements)
    
    prog = QProg()
    
    for i in range(cycles):
        prog.insert(RY(q[0], e))
        if bomb_live:
            prog.insert(Measure(q[0], c[i]))
    
    prog.insert(Measure(q[0], c[measurements - 1]))
    
    result = run_with_configuration(machine, prog, c, shots)
    counts = result
    
    if bomb_live:
        for key, value in counts.items():
            # Convert key to string representation to check bits
            bit_str = key
            if bit_str[0] == '1':  # First bit indicates detonation
                detonations += value
            elif '1' in bit_str[1:]:  # Any other bit being 1 means dud prediction
                dud_predictions += value
            else:  # All zeros means live prediction
                live_predictions += value
    else:
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1'] if '1' in counts else 0
        detonations = 0
    
    destroy_quantum_machine(machine)
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
