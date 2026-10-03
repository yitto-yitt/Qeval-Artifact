# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    q = cirq.LineQubit.range(5)
    
    full_linear_circuit = cirq.Circuit(
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[2]),
        cirq.CNOT(q[2], q[3]),
        cirq.CNOT(q[3], q[4])
    )
    full_unitary = cirq.unitary(full_linear_circuit)
    full_gate = cirq.MatrixGate(full_unitary)
    
    block1_circuit = cirq.Circuit(
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[1], q[2])
    )
    block1_unitary = cirq.unitary(block1_circuit)
    block1_gate = cirq.MatrixGate(block1_unitary)
    
    block2_circuit = cirq.Circuit(
        cirq.CNOT(q[2], q[3]),
        cirq.CNOT(q[3], q[4])
    )
    block2_unitary = cirq.unitary(block2_circuit)
    block2_gate = cirq.MatrixGate(block2_unitary)
    
    full_circuit = cirq.Circuit(
        cirq.H(q[0]),
        full_gate.on(*q)
    )
    
    limited_circuit = cirq.Circuit(
        cirq.H(q[0]),
        block1_gate.on(q[0], q[1], q[2]),
        block2_gate.on(q[2], q[3], q[4])
    )
    
    return full_circuit, limited_circuit
