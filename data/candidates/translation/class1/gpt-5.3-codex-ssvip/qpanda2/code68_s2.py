# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
import math
import builtins

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = math.pi / cycles

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(1)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        c = machine.cAlloc_many(cycles + 1)
        prog = pq.QProg()
        for i in range(cycles):
            prog.insert(pq.RY(q[0], e))
            prog.insert(pq.Measure(q[0], c[i]))
        prog.insert(pq.Measure(q[0], c[cycles]))

        counts = pq.run_with_configuration(prog, c, shots)
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        c = machine.cAlloc_many(1)
        prog = pq.QProg()
        for _ in range(cycles):
            prog.insert(pq.RY(q[0], e))
        prog.insert(pq.Measure(q[0], c[0]))

        counts = pq.run_with_configuration(prog, c, shots)
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1'] if '1' in counts else 0
        detonations = 0

    pq.destroy_quantum_machine(machine)

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
