# EVAL_META: task_id=7, framework=qiskit, class=3

from qiskit.circuit import QuantumCircuit, Parameter

def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QuantumCircuit(1)
    quantum_circuit.rx(theta, 0)
    return quantum_circuit


# ==================================================
