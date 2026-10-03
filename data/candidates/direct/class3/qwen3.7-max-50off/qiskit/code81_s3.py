# EVAL_META: task_id=81, framework=qiskit, class=3
import qiskit
import qiskit.qasm2
from qiskit import QuantumCircuit

def convert_qasm_string_to_quantum_circuit():
    qasm_str = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
"""
    if hasattr(qiskit, 'qasm2'):
        return qiskit.qasm2.loads(qasm_str)
    return QuantumCircuit.from_qasm_str(qasm_str)
