# EVAL_META: task_id=0, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)


def create_quantum_circuit(n_qubits):
    if not isinstance(n_qubits, int):
        raise TypeError("n_qubits must be an integer")
    if n_qubits < 0:
        raise ValueError("n_qubits must be nonnegative")
    return QCircuit()


machine.finalize()
