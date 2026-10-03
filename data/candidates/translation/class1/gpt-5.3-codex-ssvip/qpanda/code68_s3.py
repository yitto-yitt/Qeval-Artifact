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
        for _ in range(shots):
            machine.reset_all_qubits()
            detonated = False
            dud = False

            for _ in range(cycles):
                prog_step = QProg()
                prog_step << RY(q, e)
                machine.directly_run(prog_step)

                mprog = QProg()
                ctmp = machine.cAlloc()
                mprog << Measure(q, ctmp)
                machine.directly_run(mprog)
                mres = machine.getCBitValue(ctmp)
                machine.cFree(ctmp)

                if mres == 1:
                    detonations += 1
                    detonated = True
                    break
                else:
                    dud = True

            if not detonated:
                if dud:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        prog = QProg()
        for _ in range(cycles):
            prog << RY(q, e)
        c = machine.cAlloc()
        prog << Measure(q, c)
        result = machine.run_with_configuration(prog, [c], shots)
        machine.cFree(c)

        live_predictions = result.get("0", 0)
        dud_predictions = result.get("1", 0)
        detonations = 0

    machine.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
