# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, U3


def controlled_custom_unitary_circuit():
    machine = CPUQVM()
    qubits = machine.qAlloc_many(2)

    circuit = QCircuit()
    custom_gate = U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]])
    circuit << custom_gate

    return circuit
