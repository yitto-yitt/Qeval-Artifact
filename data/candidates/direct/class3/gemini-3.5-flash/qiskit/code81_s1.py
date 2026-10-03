# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit.qasm2 import loads

def convert_qasm_string_to_quantum_circuit():
    qasm_str = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];"""
    return loads(qasm_str)
