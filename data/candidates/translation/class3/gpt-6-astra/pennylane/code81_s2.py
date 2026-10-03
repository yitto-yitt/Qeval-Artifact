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
    next_wire = 0
    with qml.tape.QuantumTape() as circuit:
        for statement in qasm_string.split(";"):
            statement = statement.strip()
            if not statement or statement.startswith(
                ("OPENQASM", "include", "creg")
            ):
                continue

            declaration = re.fullmatch(r"qreg\s+(\w+)\[(\d+)\]", statement)
            if declaration:
                name, size = declaration.groups()
                size = int(size)
                registers[name] = list(range(next_wire, next_wire + size))
                next_wire += size
                continue

            gate, operands = statement.split(None, 1)
            wires = [
                registers[name][int(index)]
                for name, index in re.findall(r"(\w+)\[(\d+)\]", operands)
            ]
            if gate == "h":
                qml.Hadamard(wires=wires[0])
            elif gate == "cx":
                qml.CNOT(wires=wires)
            else:
                raise ValueError(f"Unsupported QASM instruction: {statement}")

    return circuit
