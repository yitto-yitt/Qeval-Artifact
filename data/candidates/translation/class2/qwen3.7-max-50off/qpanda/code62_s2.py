# EVAL_META: task_id=62, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    circuit = QuantumCircuit(num_qubits)
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.x(i)
        if basis[i] == 1:
            circuit.h(i)
    return circuit
