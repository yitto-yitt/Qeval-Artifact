# EVAL_META: task_id=117, framework=cirq, class=3
import cirq
import numpy as np

def decompose_unitary(unitary):
    # Create two qubits for the decomposition
    q0, q1 = cirq.LineQubit.range(2)
    
    # Use cirq's optimizer to decompose the unitary into a circuit with CNOT gates
    circuit = cirq.Circuit()
    circuit.append(cirq.MatrixGate(unitary).on(q0, q1))
    
    # Decompose into CNOT + single-qubit gates
    decomposed_circuit = cirq.decompose_once(circuit, keep=lambda op: True)
    final_circuit = cirq.Circuit(decomposed_circuit)
    
    # Optimize to use CNOT as basis gate where possible
    cnot_decomposed = cirq.Circuit(cirq.decompose(
        circuit,
        keep=lambda op: isinstance(op.gate, (cirq.CNOT, cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate, cirq.PhasedXPowGate)),
        on_stuck_raise=None
    ))
    
    return cnot_decomposed
