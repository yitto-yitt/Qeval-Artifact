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
    cbit = machine.cAlloc_many(measurements)
    
    prog = pq.QProg()
    
    for i in range(cycles):
        prog.insert(pq.RY(qubits[0], e))
        if bomb_live:
            prog.insert(pq.Measure(qubits[0], cbit[i]))
    
    prog.insert(pq.Measure(qubits[0], cbit[measurements - 1]))
    
    result = machine.run_with_configuration(prog, cbit, shots)
    
    if bomb_live:
        for key, value in result.items():
            # Convert key to string representation for analysis
            bits = key.replace(' ', '')
            if bits[0] == '1':
                detonations += value
            elif '1' in bits[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        # For dud case, measure final state
        for key, value in result.items():
            bits = key.replace(' ', '')
            if bits == '0':
                live_predictions += value
            else:
                dud_predictions += value
        detonations = 0
    
    machine.finalize()
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
