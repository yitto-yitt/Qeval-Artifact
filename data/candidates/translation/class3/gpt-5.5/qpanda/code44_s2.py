# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import *

def tensor_circuits():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)

    circuit = QCircuit()
    try:
        circuit.insert(RY(qubits[2], 0.2).control([qubits[1]]))
    except Exception:
        circuit.insert(RY(qubits[2], 0.1))
        circuit.insert(CNOT(qubits[1], qubits[2]))
        circuit.insert(RY(qubits[2], -0.1))
        circuit.insert(CNOT(qubits[1], qubits[2]))

    circuit.insert(X(qubits[0]))

    if not hasattr(tensor_circuits, "_machines"):
        tensor_circuits._machines = []
    tensor_circuits._machines.append(machine)

    return circuit
