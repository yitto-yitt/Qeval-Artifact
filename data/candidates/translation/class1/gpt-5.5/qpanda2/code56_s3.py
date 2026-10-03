# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def not_gate(a):
    shots = 1000
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(16)
        cbits = qvm.cAlloc_many(16)

        calib_qubits = qubits[:8]
        calib_cbits = cbits[:8]
        calib_prog = QProg()
        calib_prog << X(calib_qubits[0])
        for i in range(8):
            calib_prog << Measure(calib_qubits[i], calib_cbits[i])
        calib_counts = qvm.run_with_configuration(calib_prog, calib_cbits, 1)
        calib_key = next(iter(calib_counts.keys()))
        reverse_keys = len(calib_key) == 8 and calib_key[0] == "1"

        target_qubits = qubits[8:16]
        target_cbits = cbits[8:16]
        prog = QProg()
        a = format(a, "08b")
        for i in range(8):
            if a[7 - i] == "0":
                prog << X(target_qubits[i])
        for i in range(8):
            prog << Measure(target_qubits[i], target_cbits[i])

        counts = qvm.run_with_configuration(prog, target_cbits, shots)
        total = builtins.sum(counts.values())

        if reverse_keys:
            return {key[::-1]: value / total for key, value in counts.items()}
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
