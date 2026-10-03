# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)

    prog = qvm.qprog_init() if hasattr(qvm, "qprog_init") else None

    from pyqpanda import QProg, measure_all
    prog = QProg()

    xor_val = a ^ b
    for i in range(8):
        if (xor_val >> i) & 1:
            prog << X(qubits[i])

    prog << measure_all(qubits, cbits)

    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
