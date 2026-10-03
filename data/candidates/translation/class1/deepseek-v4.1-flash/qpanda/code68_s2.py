# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, Qubit, CBit, measure, RY, CPUQVM
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    q = Qubit(0)
    cbits = [CBit(i) for i in range(measurements)]
    
    circ = QCircuit()
    for i in range(cycles):
        circ << RY(q, e)
        if bomb_live:
            circ << measure(q, cbits[i])
    circ << measure(q, cbits[measurements - 1])
    
    prog = QProg()
    prog << circ
    
    qvm = CPUQVM()
    qvm.run(prog, shots)
    result = qvm.result()
    counts = result.get_counts()
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
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
