# EVAL_META: task_id=61, framework=qiskit, class=1

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def create_quantum_circuit_with_one_qubit_and_measure() -> QuantumCircuit:
    """
    Build a QuantumCircuit by first creating one Quantum Register and one Classical Register 
    and then performing measurement on it.
    
    Returns:
        QuantumCircuit: The constructed quantum circuit.
    """
    qr = QuantumRegister(1, name='q')
    cr = ClassicalRegister(1, name='c')
    qc = QuantumCircuit(qr, cr)
    qc.measure(qr[0], cr[0])
    return qc
