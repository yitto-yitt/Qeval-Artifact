# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QVM, QProg, H, CNOT, Measure

def bell_each_shot():
    qvm = QVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)

        prog = QProg()
        prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

        counts = qvm.run_with_configuration(prog, cbits, 10)
        total = sum(counts.values())

        return {
            key.replace(' ', '').replace(',', ''): value / total
            for key, value in counts.items()
        }
    finally:
        qvm.finalize()
