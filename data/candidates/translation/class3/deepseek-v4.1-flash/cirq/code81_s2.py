# EVAL_META: task_id=81, framework=cirq, class=3
import cirq

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
"""
    try:
        from cirq.contrib.qasm_import import circuit_from_qasm
        return circuit_from_qasm(qasm_string)
    except ImportError:
        q = [cirq.NamedQubit(f'q_{i}') for i in range(2)]
        return cirq.Circuit(cirq.H(q[0]), cirq.CNOT(q[0], q[1]))
