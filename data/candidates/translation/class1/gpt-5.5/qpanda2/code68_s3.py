# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from math import pi
import pyqpanda as pq

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    try:
        leftmost_is_first_cbit = True
        if bomb_live:
            cal_q = qvm.qAlloc_many(2)
            cal_c = qvm.cAlloc_many(2)
            cal_prog = pq.QProg()
            cal_prog << pq.X(cal_q[0])
            cal_prog << pq.Measure(cal_q[0], cal_c[0])
            cal_prog << pq.Measure(cal_q[1], cal_c[1])
            cal_counts = qvm.run_with_configuration(cal_prog, cal_c, 1)
            cal_key = str(next(iter(cal_counts.keys()))).replace(" ", "")
            if len(cal_key) == 2:
                leftmost_is_first_cbit = (cal_key == "10")

        qubits = qvm.qAlloc_many(1)
        cbits = qvm.cAlloc_many(measurements)
        prog = pq.QProg()

        for i in range(cycles):
            prog << pq.RY(qubits[0], e)
            if bomb_live:
                prog << pq.Measure(qubits[0], cbits[i])

        prog << pq.Measure(qubits[0], cbits[measurements - 1])

        counts = qvm.run_with_configuration(prog, cbits, shots)

        if bomb_live:
            final_index = measurements - 1 if leftmost_is_first_cbit else 0
            for key, value in counts.items():
                bitstring = str(key).replace(" ", "")
                if len(bitstring) < measurements:
                    bitstring = bitstring.zfill(measurements)
                if bitstring[final_index] == "1":
                    detonations += value
                elif "1" in (bitstring[:final_index] + bitstring[final_index + 1:]):
                    dud_predictions += value
                else:
                    live_predictions += value
        else:
            for key, value in counts.items():
                bitstring = str(key).replace(" ", "")
                if len(bitstring) < 1:
                    bitstring = bitstring.zfill(1)
                if bitstring[0] == "0":
                    live_predictions += value
                else:
                    dud_predictions += value
            detonations = 0

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
    finally:
        qvm.finalize()
