# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine, RY, Measure
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    qmachine = QMachine()
    q = qmachine.allocate_qubits(1)
    num_c = cycles + 1 if bomb_live else 1
    c = qmachine.allocate_cbits(num_c)
    
    circuit = QuantumCircuit()
    for i in range(cycles):
        circuit << RY(q[0], e)
        if bomb_live:
            circuit << Measure(q[0], c[i])
            
    circuit << Measure(q[0], c[num_c - 1])
    
    qmachine.apply_circuit(circuit)
    counts = qmachine.measure(shots)
    
    live_predictions = dud_predictions = detonations = 0
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
