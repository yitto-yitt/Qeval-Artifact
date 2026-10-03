# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Determine the unitary matrix and wire order of the input circuit
    if isinstance(circuit, qml.QNode):
        original_wires = circuit.device.wires
        num_qubits = len(original_wires)
        original_matrix = qml.matrix(circuit)()
    else:
        # Assume circuit is a QuantumTape
        tape = circuit
        original_wires = tape.wires
        num_qubits = len(original_wires)
        # Remove measurements if present for matrix computation
        if tape.measurements:
            with qml.tape.QuantumTape() as op_tape:
                for op in tape.operations:
                    qml.apply(op)
            original_matrix = qml.matrix(op_tape)
        else:
            original_matrix = qml.matrix(tape)
    
    wires_list = list(original_wires)
    qc_list = []
    counter = 0
    while counter < n:
        # Generate a random Clifford circuit
        with qml.tape.QuantumTape() as new_tape:
            # Ensure the tape has all wires in the same order as the original
            for w in wires_list:
                qml.Identity(wires=w)
            # Random depth: enough to generate a random Clifford
            depth = np.random.randint(1, 3 * num_qubits + 5)
            for _ in range(depth):
                # Random single-qubit Clifford gate
                wire = np.random.choice(wires_list)
                gate = np.random.choice(['H', 'S', 'X', 'Y', 'Z'])
                if gate == 'H':
                    qml.Hadamard(wires=wire)
                elif gate == 'S':
                    qml.S(wires=wire)
                elif gate == 'X':
                    qml.PauliX(wires=wire)
                elif gate == 'Y':
                    qml.PauliY(wires=wire)
                elif gate == 'Z':
                    qml.PauliZ(wires=wire)
                # Random two-qubit Clifford gate (CNOT)
                if num_qubits > 1 and np.random.rand() < 0.5:
                    ctrl = np.random.choice(wires_list)
                    tgt = np.random.choice(wires_list)
                    while tgt == ctrl:
                        tgt = np.random.choice(wires_list)
                    qml.CNOT(wires=[ctrl, tgt])
        new_matrix = qml.matrix(new_tape)
        # Check equivalence with rtol=0.4, atol=0.4
        if np.allclose(new_matrix, original_matrix, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(new_tape)
    return qc_list
