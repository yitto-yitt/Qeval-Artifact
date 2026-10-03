# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle):
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    
    circuit = cirq.Circuit()
    # Apply X to the last qubit
    circuit.append(cirq.X(qubits[-1]))
    # Apply H to all qubits
    circuit.append(cirq.H.on_each(qubits))
    # Append the oracle
    circuit.append(oracle)
    # Apply H to all qubits
    circuit.append(cirq.H.on_each(qubits))
    # Measure the first n-1 qubits in reverse order to match Qiskit's little-endianness
    measured_qubits = qubits[:-1][::-1]
    circuit.append(cirq.measure(*measured_qubits, key='result'))
    
    # Run the simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    counts = result.histogram(key='result')
    total = sum(counts.values())
    
    return {format(val, f'0{n-1}b'): count / total for val, count in counts.items()}
