# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit


def w_state():
    qc = QuantumCircuit(3, 3)
    
    # Initialize the W state: (|100> + |010> + |001>)/sqrt(3)
    # Apply operations to create the W state
    qc.ry(2 * 0.9553, 0)  # ry(2*arccos(1/sqrt(3))) on qubit 0
    qc.cx(0, 1)           # CNOT from qubit 0 to qubit 1
    qc.ry(2 * 0.6155, 2)  # ry(2*arccos(1/2)) on qubit 2
    qc.cx(1, 2)           # CNOT from qubit 1 to qubit 2
    qc.cx(0, 1)           # Reverse CNOT
    qc.x(0)               # X gate on qubit 0
    qc.cx(0, 2)           # CNOT from qubit 0 to qubit 2
    
    # Measure all qubits
    qc.measure_all()
    
    return qc
