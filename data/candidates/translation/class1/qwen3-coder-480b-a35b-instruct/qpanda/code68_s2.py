# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
from pyqpanda3 import *
import math

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
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    
    prog << Measure(q[0], c[measurements - 1])
    
    result = run_with_configuration(prog, c, shots)
    
    counts = result
    if bomb_live:
        for key, value in counts.items():
            bit_str = key
            if bit_str[0] == '1':
                detonations += value
            elif '1' in bit_str[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1']
        detonations = 0
        
    destroy_quantum_machine(machine)
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
