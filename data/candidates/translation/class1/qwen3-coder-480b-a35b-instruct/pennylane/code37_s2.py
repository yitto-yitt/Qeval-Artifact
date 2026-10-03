# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml
from collections import Counter


def bv_algorithm(s):
    n = len(s)
    
    dev = qml.device("default.qubit", wires=n+1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize ancilla qubit to |1>
        qml.PauliX(wires=n)
        
        # Apply Hadamard to all qubits
        for i in range(n+1):
            qml.Hadamard(wires=i)
        
        # Apply CNOT gates based on secret string s
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
        
        # Apply Hadamard to input register
        for i in range(n):
            qml.Hadamard(wires=i)
        
        # Measure the input register
        return [qml.sample(wires=i) for i in range(n)]
    
    samples = circuit()
    bitstring = "".join(str(int(sample)) for sample in samples)
    bitstrings = [bitstring]
    
    # Create a mock result object similar to Qiskit's structure
    class MockResult:
        def __init__(self):
            self.data = MockData()
    
    class MockData:
        def __init__(self):
            self.meas = MockMeas()
    
    class MockMeas:
        def get_bitstrings(self):
            return bitstrings
    
    result = MockResult()
    
    return [bitstrings, result]
