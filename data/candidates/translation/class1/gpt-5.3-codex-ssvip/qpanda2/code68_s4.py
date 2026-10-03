# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = math.pi / cycles

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(cycles + 1 if bomb_live else 1)

    prog = pq.QProg()
    for i in range(cycles):
        prog << pq.RY(q[0], e)
        if bomb_live:
            prog << pq.Measure(q[0], c[i])
    prog << pq.Measure(q[0], c[(cycles if bomb_live else 0)])

    counts = machine.run_with_configuration(prog, c, shots)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for key, value in counts.items():
            bitstr = key.replace(" ", "")
            if len(bitstr) < cycles + 1:
                bitstr = bitstr.zfill(cycles + 1)
            if bitstr[0] == '1':
                detonations += value
            elif '1' in bitstr[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0

    pq.destroy_quantum_machine(machine)

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
