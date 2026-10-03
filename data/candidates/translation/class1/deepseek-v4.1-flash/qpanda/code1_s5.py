# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << measure(qubits[0], cbits[0])
    prog << measure(qubits[1], cbits[1])

    counts = qvm.run_with_configuration(prog, cbits, 1000)
    qvm.finalize()

    total = sum(counts.values())
    return {str(key).zfill(2): value / total for key, value in counts.items()}
