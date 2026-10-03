# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    # Calculate number of qubits needed
    num_qubits = int(np.log2(len(diag)))
    
    # Create qubits
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    
    # Create diagonal gate using cirq.DiagonalGate
    diagonal_gate = cirq.DiagonalGate(diag)
    
    # Create circuit and append the diagonal gate
    circuit = cirq.Circuit()
    circuit.append(diagonal_gate.on(*qubits))
    
    return circuit
