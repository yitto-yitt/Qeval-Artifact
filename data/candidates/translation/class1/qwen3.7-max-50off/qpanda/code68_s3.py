# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, ry, measure
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    qm = QuantumMachine()
    q = qm.qAlloc(1)
    c = qm.cAlloc(measurements)
    
    prog = QProg()
    for i in range(cycles):
        prog << ry(q[0], e)
        if bomb_live:
            prog << measure(q[0], c[i])
    prog << measure(q[0], c[measurements - 1])
    
    counts = qm.run(prog, shots=shots)
    
    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
