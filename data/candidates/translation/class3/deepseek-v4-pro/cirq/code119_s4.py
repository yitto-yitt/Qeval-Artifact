# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Determine number of qubits based on adder type
    if kind == 'full':
        num_qubits = 2 * num_state_qubits + 1 + num_state_qubits - 1
    elif kind == 'half':
        num_qubits = 2 * num_state_qubits + num_state_qubits - 1
    elif kind == 'fixed':
        num_qubits = 2 * num_state_qubits + num_state_qubits - 1
    else:
        raise ValueError(f"Unsupported kind: {kind}")

    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    circuit = cirq.Circuit()

    # Define the majority (MAJ) gate
    def MAJ(a, b, c):
        circuit.append([cirq.CNOT(a, c), cirq.CNOT(b, c), cirq.CCNOT(a, b, c)])
        # Decomposition: CX a,c; CX b,c; CCX a,b,c
        # Equivalent unitary as CDKMRippleCarryAdder MAJ
        circuit.append([cirq.X(a), cirq.X(b), cirq.X(c)])
        circuit.append([cirq.CNOT(a, c), cirq.CNOT(b, c), cirq.CCNOT(a, b, c)])
        circuit.append([cirq.X(a), cirq.X(b), cirq.X(c)])

    # Define the UnMajority and Add (UMA) gate
    def UMA(a, b, c):
        circuit.append([cirq.CCNOT(a, b, c), cirq.CNOT(a, b), cirq.CNOT(b, c)])
        # Decomposition: CCX a,b,c; CX a,b; CX b,c
        circuit.append([cirq.X(a), cirq.X(b)])
        circuit.append([cirq.CCNOT(a, b, c), cirq.CNOT(a, b), cirq.CNOT(b, c)])
        circuit.append([cirq.X(a), cirq.X(b)])

    # Qubit layout:
    # A = a[0..n-1], B = b[0..n-1], carry = c[0..n-1] (or z), ancilla for 'full' at end
    if kind == 'full':
        # n = num_state_qubits
        n = num_state_qubits
        # a: 0..n-1, b: n..2n-1, carry: 2n..2n+n-2, ancilla: 2n+n-1
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        c = [qubits[2 * n + i] for i in range(n - 1)]
        z = qubits[2 * n + n - 1]  # ancilla
        c_in = qubits[2 * n]  # first carry is c_in

        # MAJ cascade
        MAJ(c_in, b[0], a[0])
        for i in range(1, n):
            MAJ(c[i - 1], b[i], a[i])

        # Final CNOT and UMA cascade
        circuit.append(cirq.CNOT(a[n - 1], z))
        for i in range(n - 1, 0, -1):
            UMA(c[i - 1], b[i], a[i])

    elif kind == 'half':
        n = num_state_qubits
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        c = [qubits[2 * n + i] for i in range(n - 1)]
        c_in = qubits[2 * n]

        MAJ(c_in, b[0], a[0])
        for i in range(1, n):
            MAJ(c[i - 1], b[i], a[i])

        for i in range(n - 1, 0, -1):
            UMA(c[i - 1], b[i], a[i])

    elif kind == 'fixed':
        n = num_state_qubits
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        c = [qubits[2 * n + i] for i in range(n - 1)]
        c_in = qubits[2 * n]

        MAJ(c_in, b[0], a[0])
        for i in range(1, n):
            MAJ(c[i - 1], b[i], a[i])

        for i in range(n - 1, 0, -1):
            UMA(c[i - 1], b[i], a[i])

    return circuit
