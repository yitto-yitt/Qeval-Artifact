# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QuantumMachine, QCircuit, X


def create_state_prep():
    machine = QuantumMachine()
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << X(qubits[0])
    return circuit
