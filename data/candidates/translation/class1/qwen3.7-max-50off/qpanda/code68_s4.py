# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    machine = QMachine()
    q = machine.allocate_qubits(1)
    c = machine.allocate_cbits(measurements)
    
    circuit = QuantumCircuit(q, c)
    
    for i in range(cycles):
        circuit.ry(e, q[0])
        if bomb_live:
            circuit.measure(q[0], c[i])
    circuit.measure(q[0], c[measurements - 1])
    
    result = machine.run(circuit, shots)
    counts = result.get_counts()
    
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
