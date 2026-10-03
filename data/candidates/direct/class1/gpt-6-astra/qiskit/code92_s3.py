# EVAL_META: task_id=92, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState


def calculate_stabilizer_state_info():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    return StabilizerState(circuit).probabilities_dict()
