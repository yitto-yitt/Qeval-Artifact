# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        num_qubits = 2 * n + 2
    elif kind == 'half':
        num_qubits = 2 * n + 1
    elif kind == 'fixed':
        num_qubits = 2 * n + 1
    else:
        raise ValueError("Invalid kind. Must be 'full', 'half', or 'fixed'.")

    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit():
        # Define MAJ and UMA helper functions
        def maj(c, b, a):
            qml.CNOT(wires=[a, b])
            qml.CNOT(wires=[a, c])
            qml.Toffoli(wires=[c, b, a])

        def uma(c, b, a):
            qml.Toffoli(wires=[c, b, a])
            qml.CNOT(wires=[a, c])
            qml.CNOT(wires=[c, b])

        if kind == 'full':
            # Qubit layout: cin (0), a (1..n), b (n+1..2n), cout (2n+1)
            cin = 0
            a = list(range(1, n + 1))
            b = list(range(n + 1, 2 * n + 1))
            cout = 2 * n + 1

            # MAJ step
            maj(cin, b[0], a[0])
            for i in range(1, n):
                maj(a[i-1], b[i], a[i])

            # Carry-out
            qml.CNOT(wires=[a[n-1], cout])

            # UMA step
            for i in range(n - 1, 0, -1):
                uma(a[i-1], b[i], a[i])
            uma(cin, b[0], a[0])

        elif kind == 'fixed':
            # Qubit layout: cin (0), a (1..n), b (n+1..2n)
            cin = 0
            a = list(range(1, n + 1))
            b = list(range(n + 1, 2 * n + 1))

            # MAJ step
            maj(cin, b[0], a[0])
            for i in range(1, n):
                maj(a[i-1], b[i], a[i])

            # UMA step
            for i in range(n - 1, 0, -1):
                uma(a[i-1], b[i], a[i])
            uma(cin, b[0], a[0])

        elif kind == 'half':
            # Qubit layout: a (0..n-1), b (n..2n-1), cout (2n)
            a = list(range(0, n))
            b = list(range(n, 2 * n))
            cout = 2 * n

            if n == 1:
                qml.Toffoli(wires=[a[0], b[0], cout])
                qml.CNOT(wires=[a[0], b[0]])
            else:
                # We can implement the half-adder by computing the first carry
                # into cout, and then using cout as the carry-in for the next stages.
                # Since we need cout to hold the final carry at the end, we perform
                # the addition, copy the final carry, and reverse the steps.
                
                # First stage carry-in is effectively 0, so we do:
                qml.Toffoli(wires=[a[0], b[0], cout]) # cout now holds c1
                qml.CNOT(wires=[a[0], b[0]])          # b0 holds s0

                # MAJ step for remaining stages
                for i in range(1, n):
                    if i == 1:
                        maj(cout, b[i], a[i])
                    else:
                        maj(a[i-1], b[i], a[i])

                # Now the final carry-out is in a[n-1].
                # But we need it to be in cout.
                # To do this reversibly without losing cout's intermediate value,
                # we swap the final carry-out with the temporary carry-in.
                # In Qiskit, the half adder uses the exact CDKM structure with cin=0.
                # We can simulate this by running the full adder with an auxiliary 0 qubit,
                # but since we must use exactly 2n+1 qubits, we can use the following gate sequence:
                qml.CNOT(wires=[a[n-1], cout])

                # UMA step for remaining stages
                for i in range(n - 1, 0, -1):
                    if i == 1:
                        uma(cout, b[i], a[i])
                    else:
                        uma(a[i-1], b[i], a[i])

                # Clean up the first stage
                qml.CNOT(wires=
[a
