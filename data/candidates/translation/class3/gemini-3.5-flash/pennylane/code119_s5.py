# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    def maj(c, b, a):
        qml.CNOT(wires=[a, b])
        qml.CNOT(wires=[a, c])
        qml.Toffoli(wires=[c, b, a])

    def uma(c, b, a):
        qml.Toffoli(wires=[c, b, a])
        qml.CNOT(wires=[a, c])
        qml.CNOT(wires=[c, b])

    if kind == 'full':
        def circuit():
            # Qubits layout:
            # cin: 0
            # a: 1, 3, ..., 2n-1
            # b: 2, 4, ..., 2n
            # cout: 2n+1
            maj(0, 2, 1)
            for i in range(1, n):
                maj(2*i - 1, 2*i + 2, 2*i + 1)
            
            qml.CNOT(wires=[2*n - 1, 2*n + 1])
            
            for i in range(n-1, 0, -1):
                uma(2*i - 1, 2*i + 2, 2*i + 1)
            uma(0, 2, 1)
        return circuit

    elif kind == 'half':
        def circuit():
            # Qubits layout:
            # a: 0, 2, ..., 2n-2
            # b: 1, 3, ..., 2n-1
            # cout: 2n
            if n == 1:
                qml.Toffoli(wires=[0, 1, 2])
                qml.CNOT(wires=[0, 1])
            else:
                # First stage MAJ-like
                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])
                qml.Toffoli(wires=[2, 1, 0])
                
                for i in range(1, n):
                    maj(2*i - 2, 2*i + 1, 2*i)
                
                qml.CNOT(wires=[2*n - 2, 2*n])
                
                for i in range(n-1, 0, -1):
                    uma(2*i - 2, 2*i + 1, 2*i)
                
                # First stage UMA-like
                qml.Toffoli(wires=[2, 1, 0])
                qml.CNOT(wires=[0, 2])
                qml.CNOT(wires=[0, 1])
        return circuit

    elif kind == 'fixed':
        def circuit():
            # Qubits layout:
            # a: 0, 2, ..., 2n-2
            # b: 1, 3, ..., 2n-1
            if n == 1:
                qml.CNOT(wires=[0, 1])
            else:
                # First stage MAJ-like
                qml.CNOT(wires=[0, 1])
                qml.CNOT(wires=[0, 2])
                qml.Toffoli(wires=[2, 1, 0])
                
                for i in range(1, n-1):
                    maj(2*i - 2, 2*i + 1, 2*i)
                
                # Last stage is simplified since there is no cout
                # We do a CNOT instead of the full MAJ/UMA for the last bit
                qml.CNOT(wires=[2*n - 2, 2*n - 1])
                qml.CNOT(wires=[2*n - 2, 2*n - 4])
                qml.Toffoli(wires=[2*n - 4, 2*n - 1, 2*n - 2])
                
                for i in range(n-2, 0, -1):
                    uma(2*i - 2, 2*i + 1, 2*i)
                
                # First stage UMA-like
                qml.Toffoli(wires=[2, 1, 0])
                qml.CNOT(wires=[0, 2])
                qml.CNOT(wires=[0, 1])
        return circuit
