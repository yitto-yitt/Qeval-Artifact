# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QMachineFactory, QProg, X

def xor_gate(a, b):
    qvm = QMachineFactory.create_CPU_quantum_machine()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)

    prog = QProg()
    value = a ^ b
    for i in range(8):
        if (value >> i) & 1:
            prog << X(qubits[i])

    probs = qvm.prob_run_dict(prog, qubits)
    qvm.finalize()

    return {format(value, '08b'): sum(probs.values())}
