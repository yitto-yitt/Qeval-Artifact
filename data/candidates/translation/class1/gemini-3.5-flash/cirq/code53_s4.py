# EVAL_META: task_id=53, framework=cirq, class=1
import cirq

def xor_gate(a: int, b: int):
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit()
    
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            circuit.append(cirq.X(qubits[i]))
            
    circuit.append(cirq.measure(*reversed(qubits), key='m'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='m')
    
    total = sum(counts.values())
    return {f"{key:08b}": value / total for key, value in counts.items()}
