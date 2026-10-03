# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit

def tensor_circuits():
    cry_circuit = QuantumCircuit(2)
    cry_circuit.cry(0.2, 0, 1)
    x_circuit = QuantumCircuit(1)
    x_circuit.x(0)
    return cry_circuit.tensor(x_circuit)
