# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def collect_linear_blocks_with_and_without_limit():
    ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4])
    ]
    
    cx_gates = [(op.wires[0], op.wires[1]) for op in ops if op.name == 'CNOT']
    
    def block_unitary(cx_gates):
        qubits = sorted(set([q for gate in cx_gates for q in gate]))
        local_map = {q: i for i, q in enumerate(qubits)}
        with qml.tape.QuantumTape() as tape:
            for c, t in cx_gates:
                qml.CNOT(wires=[local_map[c], local_map[t]])
        return qml.matrix(tape, wire_order=list(range(len(qubits)))), qubits
    
    def collect_blocks(cx_gates, max_width=None):
        if max_width is None:
            return [cx_gates]
        blocks = []
        current_block = []
        current_qubits = set()
        for gate in cx_gates:
            c, t = gate
            new_qubits = current_qubits | {c, t}
            if len(new_qubits) > max_width:
                if current_block:
                    blocks.append(current_block)
                current_block = [gate]
                current_qubits = {c, t}
            else:
                current_block.append(gate)
                current_qubits = new_qubits
        if current_block:
            blocks.append(current_block)
        return blocks
    
    with qml.tape.QuantumTape() as tape_full:
        qml.Hadamard(wires=0)
        for block in collect_blocks(cx_gates, max_width=None):
            mat, qubits = block_unitary(block)
            qml.QubitUnitary(mat, wires=qubits)
    
    with qml.tape.QuantumTape() as tape_limited:
        qml.Hadamard(wires=0)
        for block in collect_blocks(cx_gates, max_width=3):
            mat, qubits = block_unitary(block)
            qml.QubitUnitary(mat, wires=qubits)
    
    return tape_full, tape_limited
