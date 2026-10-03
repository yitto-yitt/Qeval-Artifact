# EVAL_META: task_id=81, framework=cirq, class=3
from cirq.qasm_import import circuit_from_qasm

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    return circuit_from_qasm(qasm_string)
