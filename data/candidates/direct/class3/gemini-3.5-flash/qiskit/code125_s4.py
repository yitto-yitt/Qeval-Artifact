# EVAL_META: task_id=125, framework=qiskit, class=3
from qiskit import QuantumCircuit

def circ_to_gate(circ: QuantumCircuit):
    """Convert a QuantumCircuit into a Gate equivalent to the action of the input circuit."""
    return circ.to_gate()
