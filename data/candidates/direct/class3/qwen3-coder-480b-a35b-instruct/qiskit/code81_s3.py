# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit import QuantumCircuit, qasm2

def convert_qasm_string_to_quantum_circuit():
    # Create a QASM 2 string for the Phi plus Bell state (|Φ+⟩ = 1/sqrt(2)(|00⟩ + |11⟩))
    qasm_string = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];
"""
    
    # Convert the QASM string to a QuantumCircuit object
    circuit = qasm2.loads(qasm_string)
    
    return circuit
