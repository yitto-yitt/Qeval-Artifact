# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    dev = qml.device("default.qubit", wires=5)

    @qml.qnode(dev)
    def base_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
        return qml.state()

    base_circuit()
    tape = base_circuit.qtape

    full_block = qml.transforms.merge_rotations(tape)

    @qml.transform
    def limit_block_width(tape, max_block_width=3):
        new_ops = []
        cnot_chain = []
        for op in tape.operations:
            if op.name == "CNOT":
                cnot_chain.append(op)
            else:
                if cnot_chain:
                    if len(cnot_chain) > max_block_width:
                        for i in range(0, len(cnot_chain), max_block_width):
                            new_ops.extend(cnot_chain[i:i + max_block_width])
                    else:
                        new_ops.extend(cnot_chain)
                    cnot_chain = []
                new_ops.append(op)
        if cnot_chain:
            if len(cnot_chain) > max_block_width:
                for i in range(0, len(cnot_chain), max_block_width):
                    new_ops.extend(cnot_chain[i:i + max_block_width])
            else:
                new_ops.extend(cnot_chain)
        new_tape = qml.tape.QuantumTape(new_ops, tape.measurements)
        return [new_tape], lambda res: res[0]

    limited_block = limit_block_width(tape, max_block_width=3)[0][0]

    return full_block, limited_block
