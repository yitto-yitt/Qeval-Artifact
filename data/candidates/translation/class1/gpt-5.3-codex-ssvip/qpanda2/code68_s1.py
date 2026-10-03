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

    if bomb_live:
        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for _ in range(shots):
            measured_bits = []
            detonated = False

            for _ in range(cycles):
                prog = pq.QProg()
                prog << pq.RY(q[0], e)
                c = machine.cAlloc()
                prog << pq.Measure(q[0], c)
                machine.directly_run(prog)
                m = machine.getCBitValue(c)
                measured_bits.append(m)
                if m == 1:
                    detonated = True
                    break

            if detonated:
                detonations += 1
            else:
                final_bit = measured_bits[-1] if len(measured_bits) > 0 else 0
                if final_bit == 1:
                    dud_predictions += 1
                else:
                    live_predictions += 1

            machine.qFree_all(q)
            q = machine.qAlloc_many(1)

        pq.destroy_quantum_machine(machine)
        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }

    else:
        prog = pq.QProg()
        for _ in range(cycles):
            prog << pq.RY(q[0], e)
        c = machine.cAlloc()
        prog << pq.Measure(q[0], c)

        counts = machine.run_with_configuration(prog, [c], shots)
        total = builtins.sum(counts.values()) if counts else shots
        live_predictions = counts.get("0", 0)
        dud_predictions = counts.get("1", 0)
        detonations = 0

        pq.destroy_quantum_machine(machine)
        return {
            "live_predictions": live_predictions / total,
            "dud_predictions": dud_predictions / total,
            "detonations": detonations / total,
        }
