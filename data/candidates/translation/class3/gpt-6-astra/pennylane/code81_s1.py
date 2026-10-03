# EVAL_META: task_id=81, framework=pennylane, class=3
import re
import pennylane as qml


def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    operations = []
    pattern = r"\b(h|cx)\s+q\[(\d+)\](?:\s*,\s*q\[(\d+)\])?\s*;"
    for match in re.finditer(pattern, qasm_string):
        gate, first, second = match.groups()
        if gate == "h":
            operations.append(qml.Hadamard(wires=int(first)))
        else:
            operations.append(qml.CNOT(wires=[int(first), int(second)]))

    return qml.tape.QuantumScript(operations)
