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

    wire_map = {}
    for name, size in re.findall(r"qreg\s+(\w+)\[(\d+)\]\s*;", qasm_string):
        for index in range(int(size)):
            wire_map[(name, index)] = len(wire_map)

    gates = {"h": qml.Hadamard, "cx": qml.CNOT}
    operations = []
    with qml.QueuingManager.stop_recording():
        for statement in qasm_string.split(";"):
            statement = statement.strip()
            if not statement or statement.startswith(
                ("OPENQASM", "include", "qreg", "creg")
            ):
                continue
            gate, operands = statement.split(None, 1)
            wires = [
                wire_map[(name, int(index))]
                for name, index in re.findall(r"(\w+)\[(\d+)\]", operands)
            ]
            operations.append(gates[gate](wires=wires))

    return qml.tape.QuantumScript(operations)
