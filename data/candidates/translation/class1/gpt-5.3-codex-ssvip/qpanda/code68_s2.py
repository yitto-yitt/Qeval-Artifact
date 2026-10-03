# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import *

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)[0]

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        p_survive = 1.0
        for i in range(cycles):
            prog = QProg()
            prog << RY(q, e)
            prog << Measure(q, machine.cAlloc())
            result = machine.run_with_configuration(prog, [prog.get_used_cbits()[0]], shots)
            p0 = result.get("0", 0) / shots
            p1 = result.get("1", 0) / shots
            detonations += p_survive * p1
            p_survive *= p0
            machine.qFree(q)
            q = machine.qAlloc_many(1)[0]
        prog_final = QProg()
        prog_final << Measure(q, machine.cAlloc())
        result_final = machine.run_with_configuration(prog_final, [prog_final.get_used_cbits()[0]], shots)
        p0_final = result_final.get("0", 0) / shots
        p1_final = result_final.get("1", 0) / shots
        live_predictions = p_survive * p0_final
        dud_predictions = p_survive * p1_final
    else:
        prog = QProg()
        for _ in range(cycles):
            prog << RY(q, e)
        c = machine.cAlloc()
        prog << Measure(q, c)
        result = machine.run_with_configuration(prog, [c], shots)
        live_predictions = result.get("0", 0) / shots
        dud_predictions = result.get("1", 0) / shots
        detonations = 0.0

    machine.finalize()

    return {
        "live_predictions": live_predictions,
        "dud_predictions": dud_predictions,
        "detonations": detonations,
    }
