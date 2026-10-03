# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s: str) -> QuantumCircuit:
    n = len(s)
    # Create quantum and classical registers with specified name 'c'
    q_top = QuantumRegister(n, 'q')
    q_bottom = QuantumRegister(n, 'b')
    c_reg = ClassicalRegister(n, 'c')
    circuit = QuantumCircuit(q_top, q_bottom, c_reg)
    
    # Step 1: Apply Hadamard to top register
    for i in range(n):
        circuit.h(q_top[i])
    
    # Oracle U_f implementing f(x) such that f(x) = f(x ⊕ s)
    # Standard construction: f(x) = x if the first '1'-bit of s is 0 in x,
    # otherwise f(x) = x ⊕ s.
    for i in range(n):
        circuit.cx(q_top[i], q_bottom[i])
    # If s is not all zeros, find the first 1 and apply additional CNOTs
    if '1' in s:
        k = s.index('1')
        for i in range(n):
            if s[i] == '1':
                circuit.cx(q_top[k], q_bottom[i])
    
    # Step 2: Apply Hadamard to top register again
    for i in range(n):
        circuit.h(q_top[i])
    
    # Step 3: Measure top register into classical register 'c'
    for i in range(n):
        circuit.measure(q_top[i], c_reg[i])
    
    return circuit
