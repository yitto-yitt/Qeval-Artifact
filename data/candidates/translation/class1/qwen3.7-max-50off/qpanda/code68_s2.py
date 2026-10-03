# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    qc = QuantumCircuit(1, measurements)
    for i in range(cycles):
        qc.ry(e, 0)
        if bomb_live:
            qc.measure(0, i)
    qc.measure(0, measurements - 1)
    
    qvm = QMachine()
    result = qvm.run(qc, shots)
    counts = result.get_counts()
    
    if bomb_live:
        for key, value in counts.items():
            key_str = str(key)
            if len(key_str) < measurements:
                key_str = '0' * (measurements - len(key_str)) + key_str
            if key_str[0] == '1':
                detonations += value
            elif '1' in key_str[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', counts.get(0, 0))
        dud_predictions = counts.get('1', counts.get(1, 0))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
