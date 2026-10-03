# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    qvm = pyqpanda.init_quantum_machine(pyqpanda.QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(measurements)
    
    prog = pyqpanda.QProg()
    
    for i in range(cycles):
        prog << pyqpanda.RY(q[0], e)
        if bomb_live:
            prog << pyqpanda.Measure(q[0], c[i])
            
    prog << pyqpanda.Measure(q[0], c[measurements - 1])
    
    counts = qvm.run_with_configuration(prog, c, shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        for key, value in counts.items():
            key_str = str(key).zfill(measurements)
            if key_str[0] == '1':
                detonations += value
            elif '1' in key_str[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        for key, value in counts.items():
            key_str = str(key).zfill(1)
            if key_str == '0':
                live_predictions += value
            elif key_str == '1':
                dud_predictions += value
                
    qvm.finalize()
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
