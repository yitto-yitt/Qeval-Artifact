# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from numpy import pi
def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi/cycles
    measurements = cycles + 1 if bomb_live else 1
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qvec = machine.qAllocMany(1)
    cvec = machine.cAllocMany(measurements)
    prog = pq.QProg()
    for i in range(cycles):
        prog << pq.RY(qvec[0], e)
        if bomb_live:
            prog << pq.Measure(qvec[0], cvec[i])
    prog << pq.Measure(qvec[0], cvec[measurements - 1])
    counts = machine.run_with_configuration(prog, shots)
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
    machine.finalize()
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
