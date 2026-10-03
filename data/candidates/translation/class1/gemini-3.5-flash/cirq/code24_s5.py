# EVAL_META: task_id=24, framework=cirq, class=1
import cirq

def dj_algorithm(oracle: cirq.Circuit):
    qubits = sorted(list(oracle.all_qubits()))
    n = len(qubits)
    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[-1]))
    circuit.append(cirq.H.on_each(*qubits))
    circuit.append(oracle)
    circuit.append(cirq.H.on_each(*qubits))
    
    # Measure input qubits in reversed order to match Qiskit's LSB-on-the-right convention
    circuit.append(cirq.measure(*qubits[:-1][::-1], key='result'))
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1024)
    hist = result.histogram(key='result')
    total = sum(hist.values())
    
    prob_dist = {}
    for val, count in hist.items():
        bitstring = format(val, f'0{n-1}b')
        prob_dist[bitstring] = count / total
        
    return prob_dist
