# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, X, CNOT


def create_state_prep(num_qubits):
    qvm = CPUQVM()
    try:
        qvm.init_qvm()
    except AttributeError:
        pass

    qubits = qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()

    if num_qubits > 0:
        circuit << X(qubits[0])
        for i in range(1, num_qubits):
            circuit << CNOT(qubits[0], qubits[i])
            circuit << CNOT(qubits[0], qubits[i])

    if not hasattr(create_state_prep, "_qvms"):
        create_state_prep._qvms = []
    create_state_prep._qvms.append(qvm)

    return circuit
