# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(measurements)
    
    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    prog << Measure(q[0], c[measurements - 1])
    
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()
    
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        for key, value in result.items():
            reversed_key = key[::-1]
            if reversed_key[0] == '1':
                detonations += value
            elif '1' in reversed_key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = result.get('0', 0)
        dud_predictions = result.get('1', 0)
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
