# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def and_gate(a, b):
    a &= 7
    b &= 7
    
    qa = QuantumRegister(3, 'a')
    qb = QuantumRegister(3, 'b')
    qc = QuantumRegister(3, 'c')
    cr = ClassicalRegister(3, 'out')
    circuit = QuantumCircuit(qa, qb, qc, cr)
    
    for i in range(3):
        if (a >> i) & 1:
            circuit.x(qa[i])
        if (b >> i) & 1:
            circuit.x(qb[i])
    
    for i in range(3):
        circuit.ccx(qa[i], qb[i], qc[i])
    
    for i in range(3):
        circuit.measure(qc[i], cr[i])
    
    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(circuit, shots=shots).result()
    counts = result.get_counts()
    return {state: count / shots for state, count in counts.items()}
