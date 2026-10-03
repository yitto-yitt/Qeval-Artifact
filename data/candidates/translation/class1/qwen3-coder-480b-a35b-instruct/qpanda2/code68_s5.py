# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from numpy import pi
import builtins

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi/cycles
    measurements = cycles + 1 if bomb_live else 1
    
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(1)
    cbit = [machine.cAlloc() for _ in range(measurements)]
    
    prog = pq.QProg()
    
    for i in range(cycles):
        prog << pq.RY(qubits[0], e)
        if bomb_live:
            prog << pq.Measure(qubits[0], cbit[i])
    
    prog << pq.Measure(qubits[0], cbit[measurements - 1])
    
    result = machine.run_with_configuration(prog, cbit, shots)
    counts = result
    
    if bomb_live:
        for key, value in counts.items():
            key_str = key.replace(' ', '')
            if key_str[0] == '1':
                detonations += value
            elif '1' in key_str[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        key_0 = '0'
        key_1 = '1'
        live_predictions = counts[key_0] if key_0 in counts else 0
        dud_predictions = counts[key_1] if key_1 in counts else 0
        detonations = 0
    
    machine.finalize()
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
