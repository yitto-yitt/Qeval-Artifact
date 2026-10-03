# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import *

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for _ in range(shots):
            exploded = False
            for _ in range(cycles):
                prog_step = QProg()
                prog_step << RY(q[0], e) << Measure(q[0], c[0])
                machine.directly_run(prog_step)
                m = machine.getCBitValue(c[0])
                if m == 1:
                    detonations += 1
                    exploded = True
                    break
            if not exploded:
                prog_final = QProg()
                prog_final << Measure(q[0], c[0])
                machine.directly_run(prog_final)
                final_m = machine.getCBitValue(c[0])
                if final_m == 1:
                    dud_predictions += 1
                else:
                    live_predictions += 1
            machine.qReset(q[0])
    else:
        prog = QProg()
        for _ in range(cycles):
            prog << RY(q[0], e)
        prog << Measure(q[0], c[0])

        result = machine.run_with_configuration(prog, c, shots)
        live_predictions = result["0"] if "0" in result else 0
        dud_predictions = result["1"] if "1" in result else 0
        detonations = 0

    machine.finalize()
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
