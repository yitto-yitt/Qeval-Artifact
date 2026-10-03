# EVAL_META: task_id=69, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import SdgGate

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    """Build the specified circuit."""
    qc = QuantumCircuit(2)

    # H on qubit 0
    qc.h(0)
    # Controlled-S (CS) with control 0, target 1
    qc.cs(0, 1)
    # H on qubit 1
    qc.h(1)
    # Controlled-S dagger with control 1, target 0
    csdg_gate = SdgGate().control(1)
    qc.append(csdg_gate, [1, 0])

    return qc
