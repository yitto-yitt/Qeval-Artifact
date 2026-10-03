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
    
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    c = machine.cAlloc_many(measurements)
    
    prog = pq.QProg()
    
    for i in range(cycles):
        prog.insert(pq.RY(qubits[0], e))
        if bomb_live:
            prog.insert(pq.Measure(qubits[0], c[i]))
    
    prog.insert(pq.Measure(qubits[0], c[measurements - 1]))
    
    result = pq.prob_run_dict(prog, qubits, shots)
    
    if bomb_live:
        for key, value in result.items():
            # Convert binary string to check bits
            bit_str = bin(int(key))[2:].zfill(measurements)
            if bit_str[0] == '1':
                detonations += value
            elif '1' in bit_str[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        # For dud case, we have only one measurement
        for key, value in result.items():
            bit_str = bin(int(key))[2:].zfill(1)
            if bit_str[0] == '0':
                live_predictions += value
            else:
                dud_predictions += value
        detonations = 0
    
    total_shots = builtins.sum(result.values())
    
    return {
        "live_predictions": live_predictions / total_shots,
        "dud_predictions": dud_predictions / total_shots,
        "detonations": detonations / total_shots,
    }
