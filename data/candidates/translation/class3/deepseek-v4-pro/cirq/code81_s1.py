# EVAL_META: task_id=81, framework=cirq, class=3
import cirq

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    circuit = cirq.read_qasm(qasm_string)
    return circuit
