# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.qasm2 import loads

def convert_qasm_string_to_quantum_circuit():
    # QASM 2 string for Phi plus Bell state (|Φ+⟩ = 1/√2(|00⟩ + |11⟩))
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0], q[1];"""
    
    # Convert QASM string to QuantumCircuit object
    circuit = loads(qasm_string)
    return circuit
