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

    registers = {}
    offset = 0
    for name, size in re.findall(r"qreg\s+(\w+)\[(\d+)\]\s*;", qasm_string):
        registers[name] = list(range(offset, offset + int(size)))
        offset += int(size)

    gates = {"h": qml.Hadamard, "cx": qml.CNOT}
    with qml.tape.QuantumTape() as circuit:
        for gate, operands in re.findall(r"\b(h|cx)\s+([^;]+);", qasm_string):
            wires = [
                registers[name][int(index)]
                for name, index in re.findall(r"(\w+)\[(\d+)\]", operands)
            ]
            gates[gate](wires=wires)

    return circuit
