# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda import *

def create_cy_gate():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(S(qubits[1]).dagger())
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(S(qubits[1]))
    return circuit
