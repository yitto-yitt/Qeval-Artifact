# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    # Determine qubit layout and total number of qubits
    # Register order matches Qiskit CDKMRippleCarryAdder:
    # full:  [cin] + a + b + [cout]
    # half:  a + b + [cout]
    # fixed: a + b
    if kind == "full":
        num_qubits = 2 * n + 2
    elif kind == "half":
        num_qubits = 2 * n + 1
    elif kind == "fixed":
        num_qubits = 2 * n
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def MAJ(a, b, c):
        qml.CNOT(wires=[c, b])
        qml.CNOT(wires=[c, a])
        qml.Toffoli(wires=[a, b, c])

    def UMA(a, b, c):
        qml.Toffoli(wires=[a, b, c])
        qml.CNOT(wires=[c, a])
        qml.CNOT(wires=[a, b])

    def adder_ops():
        if kind == "full":
            cin = 0
            a = [1 + i for i in range(n)]
            b = [1 + n + i for i in range(n)]
            cout = 2 * n + 1
            carry_in = cin
            carry_out = cout
        elif kind == "half":
            a = [i for i in range(n)]
            b = [n + i for i in range(n)]
            cout = 2 * n
            carry_in = None
            carry_out = cout
        else:  # fixed
            a = [i for i in range(n)]
            b = [n + i for i in range(n)]
            carry_in = None
            carry_out = None

        # ripple carry register: use carry_in if present, else first a as helper
        if carry_in is not None:
            cin = carry_in
        else:
            # fixed/half: there is no explicit cin; use a[0] trick like CDKM "no cin"
            cin = None

        if cin is not None:
            MAJ(cin, b[0], a[0])
            for i in range(1, n):
                MAJ(a[i - 1], b[i], a[i])

            if carry_out is not None:
                qml.CNOT(wires=[a[n - 1], carry_out])

            for i in reversed(range(1, n)):
                UMA(a[i - 1], b[i], a[i])
            UMA(cin, b[0], a[0])
        else:
            # version without carry-in (half/fixed)
            qml.CNOT(wires=[a[0], b[0]]) if False else None
            # Use standard CDKM without cin:
            # MAJ chain starting with a[0] as its own carry origin
            qml.Toffoli(wires=[a[0], b[0], a[0]]) if False else None

            # Implement no-cin variant:
            for i in range(1, n):
                qml.CNOT(wires=[a[i], b[i]])
            if n > 1:
                qml.CNOT(wires=[a[1], a[0]])
                qml.Toffoli(wires=[a[0], b[0], a[1]])
                qml.CNOT(wires=[a[2] if n > 2 else a[1], a[1]]) if False else None

            for i in range(2, n):
                qml.CNOT(wires=[a[i], a[i - 1]])
                qml.Toffoli(wires=[a[i - 1], b[i - 1], a[i]])

            if carry_out is not None:
                qml.CNOT(wires=[a[n - 1], carry_out])
                if n > 1:
                    qml.Toffoli(wires=[a[n - 2], b[n - 1], carry_out])

            for i in reversed(range(2, n)):
                qml.Toffoli(wires=[a[i - 1], b[i - 1], a[i]])
                qml.CNOT(wires=[a[i], a[i - 1]])
                qml.CNOT(wires=[a[i - 1], b[i - 1]])

            if n > 1:
                qml.Toffoli(wires=[a[0], b[0], a[1]])
                qml.CNOT(wires=[a[1], a[0]])
            qml.CNOT(wires=[a[0], b[0]])

    qc = qml.tape.QuantumScript(
        ops=qml.tape.make_qscript(adder_ops)().operations,
        measurements=[],
    )
    return qc
