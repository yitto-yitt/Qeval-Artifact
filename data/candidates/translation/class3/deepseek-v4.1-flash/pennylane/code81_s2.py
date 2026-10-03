# EVAL_META: task_id=81, framework=pennylane, class=3
import pennylane as qml

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    with qml.tape.QuantumTape() as tape:
        qml.from_qasm(qasm_string)()
    return tape
