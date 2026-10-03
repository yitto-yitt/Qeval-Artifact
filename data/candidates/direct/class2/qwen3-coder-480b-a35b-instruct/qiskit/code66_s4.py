# EVAL_META: task_id=66, framework=qiskit, class=2
from qiskit import QuantumCircuit

def w_state():
    qc = QuantumCircuit(3, 3)
    
    # Initialize the W state: (|001> + |010> + |100>)/sqrt(3)
    # Apply operations to create the W state
    qc.ry(2 * 0.955316618, 0)  # ry(2*arccos(1/sqrt(3))) on qubit 0
    qc.cx(0, 1)
    qc.ry(2 * 0.615479709, 2)  # ry(2*arccos(1/sqrt(2))) on qubit 2
    qc.cx(1, 2)
    qc.x(1)
    qc.cx(1, 0)
    qc.cx(2, 1)
    qc.x(2)

    # Measure all qubits
    qc.measure_all()

    return qc
