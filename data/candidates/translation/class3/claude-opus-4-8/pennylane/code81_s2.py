# EVAL_META: task_id=81, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    loaded = qml.from_qasm(qasm_string)
    with qml.queuing.AnnotatedQueue() as q:
        loaded()
    circuit = QuantumScript.from_queue(q)
    return circuit
