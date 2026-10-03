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

    def circuit():
        loaded(wires=[0, 1])
        return qml.state()

    with qml.queuing.AnnotatedQueue() as q:
        circuit()

    tape = QuantumScript.from_queue(q)
    return tape
