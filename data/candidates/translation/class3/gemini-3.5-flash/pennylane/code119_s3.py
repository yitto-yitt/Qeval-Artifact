# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml

def MAJ(c, b, a):
    qml.CNOT(wires=[a, b])
    qml.CNOT(wires=[a, c])
    qml.Toffoli(wires=[c, b, a])

def UMA(c, b, a):
    qml.Toffoli(wires=[c, b, a])
    qml.CNOT(wires=[a, c])
    qml.CNOT(wires=[c, b])

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == "full":
        num_qubits = 2 * n + 2
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
        
        dev = qml.device("default.qubit", wires=num_qubits)
        
        @qml.qnode(dev)
        def circuit():
            # MAJ gates
            MAJ(cin, b[0], a[0])
            for i in range(1, n):
                MAJ(a[i-1], b[i], a[i])
            
            # Carry out
            qml.CNOT(wires=[a[n-1], cout])
            
            # UMA gates
            for i in reversed(range(1, n)):
                UMA(a[i-1], b[i], a[i])
            UMA(cin, b[0], a[0])
            
            return qml.state()
            
        return circuit

    elif kind == "fixed":
        num_qubits = 2 * n + 1
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        
        dev = qml.device("default.qubit", wires=num_qubits)
        
        @qml.qnode(dev)
        def circuit():
            # MAJ gates
            MAJ(cin, b[0], a[0])
            for i in range(1, n):
                MAJ(a[i-1], b[i], a[i])
            
            # UMA gates
            for i in reversed(range(1, n)):
                UMA(a[i-1], b[i], a[i])
            UMA(cin, b[0], a[0])
            
            return qml.state()
            
        return circuit

    elif kind == "half":
        num_qubits = 2 * n + 1
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n
        
        dev = qml.device("default.qubit", wires=num_qubits)
        
        @qml.qnode(dev)
        def circuit():
            if n == 1:
                qml.Toffoli(wires=[a[0], b[0], cout])
                qml.CNOT(wires=[a[0], b[0]])
            else:
                # First step (MAJ equivalent for half adder)
                qml.CNOT(wires=[a[0], b[0]])
                qml.CNOT(wires=[a[0], a[1]])
                qml.Toffoli(wires=[a[1], b[0], a[0]])
                
                # Remaining MAJ steps
                for i in range(1, n - 1):
                    MAJ(a[i-1], b[i], a[i])
                
                # Last MAJ step with cout
                MAJ(a[n-2], b[n-1], a[n-1])
                qml.CNOT(wires=[a[n-1], cout])
                UMA(a[n-2], b[n-1], a[n-1])
                
                # Remaining UMA steps
                for i in reversed(range(1, n - 1)):
                    UMA(a[i-1], b[i], a[i])
                
                # First step inverse (UMA equivalent)
                qml.Toffoli(wires=[a[1], b[0], a[0]])
                qml.CNOT(wires=[a[0], a[1]])
                qml.CNOT(wires=[a[0], b[0]])
                
            return qml.state()
            
        return circuit
