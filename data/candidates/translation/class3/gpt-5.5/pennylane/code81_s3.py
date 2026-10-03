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

    qasm_body = re.sub(r"//.*", "", qasm_string)
    statements = [stmt.strip() for stmt in qasm_body.split(";") if stmt.strip()]

    qreg_offsets = {}
    next_wire = 0
    ops = []

    def parse_wire(token):
        match = re.fullmatch(r"\s*([A-Za-z_]\w*)\s*\[\s*(\d+)\s*\]\s*", token)
        if match is None:
            raise ValueError(f"Invalid wire token: {token}")
        reg_name, index = match.group(1), int(match.group(2))
        return qreg_offsets[reg_name] + index

    for statement in statements:
        if statement.startswith("OPENQASM") or statement.startswith("include") or statement.startswith("creg"):
            continue

        qreg_match = re.fullmatch(r"qreg\s+([A-Za-z_]\w*)\s*\[\s*(\d+)\s*\]", statement)
        if qreg_match:
            name, size = qreg_match.group(1), int(qreg_match.group(2))
            qreg_offsets[name] = next_wire
            next_wire += size
            continue

        gate_match = re.fullmatch(r"([A-Za-z_]\w*)\s+(.+)", statement)
        if gate_match is None:
            continue

        gate = gate_match.group(1).lower()
        args = [arg.strip() for arg in gate_match.group(2).split(",")]

        if gate == "h":
            ops.append(qml.Hadamard(wires=parse_wire(args[0])))
        elif gate in {"cx", "cnot"}:
            ops.append(qml.CNOT(wires=[parse_wire(args[0]), parse_wire(args[1])]))

    return qml.tape.QuantumScript(ops, [])
