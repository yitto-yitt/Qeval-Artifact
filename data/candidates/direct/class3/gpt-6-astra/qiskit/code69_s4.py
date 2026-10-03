# EVAL_META: task_id=69, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cs(0, 1)
    circuit.h(1)
    circuit.csdg(1, 0)
    return circuit
