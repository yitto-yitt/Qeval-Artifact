# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = math.pi / cycles

    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    if bomb_live:
        for _ in range(shots):
            detonated = False
            for _ in range(cycles):
                prog = QProg()
                prog << RY(q[0], e)
                result = machine.prob_run_dict(prog, q, -1)
                p1 = result.get("1", 0.0)
                if machine.get_random_double() < p1:
                    detonations += 1
                    detonated = True
                    break
                else:
                    prog_reset = QProg()
                    prog_reset << Reset(q[0])
                    machine.directly_run(prog_reset)
            if not detonated:
                final_prog = QProg()
                final_result = machine.prob_run_dict(final_prog, q, -1)
                p1_final = final_result.get("1", 0.0)
                if machine.get_random_double() < p1_final:
                    dud_predictions += 1
                else:
                    live_predictions += 1
            reset_prog = QProg()
            reset_prog << Reset(q[0])
            machine.directly_run(reset_prog)
    else:
        prog = QProg()
        for _ in range(cycles):
            prog << RY(q[0], e)
        counts = machine.run_with_configuration(prog, q, shots)
        live_predictions = counts.get("0", 0)
        dud_predictions = counts.get("1", 0)
        detonations = 0

    machine.finalize()
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
