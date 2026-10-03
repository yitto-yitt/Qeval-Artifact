# EVAL_META: task_id=6, framework=qiskit, class=2

from qiskit import QuantumCircuit

def create_state_prep(num_qubits: int) -> QuantumCircuit:
    """Return a QuantumCircuit that prepares the state |1> on an n-qubit register.
    This prepares the state |1>^{\otimes n} (all qubits in state |1>).
    """
    qc = QuantumCircuit(num_qubits)
    qc.x(range(num_qubits))
    return qc
