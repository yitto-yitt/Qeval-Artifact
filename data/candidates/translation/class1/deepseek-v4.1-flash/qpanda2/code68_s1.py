# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    qvm = CPUQVM()
    qvm.init_qvm()
    
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(measurements)
    
    prog = QProg()
    
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    
    prog << Measure(q[0], c[measurements - 1])
    
    result = qvm.run_with_configuration(prog, c, shots)
    
    if bomb_live:
        for key, value in result.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = result.get('0', 0)
        dud_predictions = result.get('1', 0)
        detonations = 0
    
    qvm.finalize()
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
