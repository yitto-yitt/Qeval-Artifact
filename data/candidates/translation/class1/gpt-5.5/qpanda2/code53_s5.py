# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def xor_gate(a, b):
    shots = 1024
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        cal_qubits = qvm.qAlloc_many(8)
        cal_cbits = qvm.cAlloc_many(8)
        cal_prog = pq.QProg()
        cal_prog << pq.X(cal_qubits[0])
        for i in range(8):
            cal_prog << pq.Measure(cal_qubits[i], cal_cbits[i])
        cal_counts = qvm.run_with_configuration(cal_prog, cal_cbits, shots)
        cal_key = max(cal_counts, key=cal_counts.get)
        reverse_keys = len(cal_key) == 8 and cal_key[0] == "1"

        qubits = qvm.qAlloc_many(8)
        cbits = qvm.cAlloc_many(8)
        prog = pq.QProg()

        for i in range(8):
            if (int(a) >> i) & 1:
                prog << pq.X(qubits[i])
        for i in range(8):
            if (int(b) >> i) & 1:
                prog << pq.X(qubits[i])

        for i in range(8):
            prog << pq.Measure(qubits[i], cbits[i])

        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = builtins.sum(counts.values())

        probabilities = {}
        for key, value in counts.items():
            out_key = key[::-1] if reverse_keys else key
            probabilities[out_key] = probabilities.get(out_key, 0.0) + value / total

        return probabilities
    finally:
        qvm.finalize()
