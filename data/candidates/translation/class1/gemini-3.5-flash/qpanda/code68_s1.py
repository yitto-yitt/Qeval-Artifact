# EVAL_META: task_id=68, framework=qpanda, class=1
import pyqpanda3.core as pq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(measurements)
    
    prog = pq.QProg()
    for i in range(cycles):
        prog << pq.RY(q[0], e)
        if bomb_live:
            prog << pq.Measure(q[0], c[i])
    prog << pq.Measure(q[0], c[measurements - 1])
    
    counts = machine.run_with_configuration(prog, c, shots)
    
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
