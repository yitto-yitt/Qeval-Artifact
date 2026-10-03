# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit import QuantumCircuit


def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
"""
    return QuantumCircuit.from_qasm_str(qasm_string)
