# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def create_product_formula_circuit(pauli_strings, times, order, reps):
    machine = CPUQVM()
    machine.init_qvm()
    num_qubits = len(pauli_strings[0])
    try:
        qubits = machine.qAlloc_many(num_qubits)
    except AttributeError:
        qubits = machine.qAllocMany(num_qubits)
        
    circuit = QCircuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        dt = time / reps
        for _ in range(reps):
            active_qubits = []
            active_paulis = []
            for i in range(num_qubits):
                p = pauli_string[num_qubits - 1 - i]
                if p != 'I':
                    active_qubits.append(qubits[i])
                    active_paulis.append(p)
            
            if not active_qubits:
                continue
                
            # Basis change
            for q, p in zip(active_qubits, active_paulis):
                if p == 'X':
                    circuit << H(q)
                elif p == 'Y':
                    circuit << RX(q, math.pi / 2)
            
            # CNOT cascade
            k = len(active_qubits)
            for j in range(k - 1):
                circuit << CNOT(active_qubits[j], active_qubits[j+1])
                
            # RZ rotation
            circuit << RZ(active_qubits[k-1], 2 * dt)
            
            # Reverse CNOT cascade
            for j in range(k - 2, -1, -1):
                circuit << CNOT(active_qubits[j], active_qubits[j+1])
                
            # Inverse basis change
            for q, p in zip(active_qubits, active_paulis):
                if p == 'X':
                    circuit << H(q)
                elif p == 'Y':
                    circuit << RX(q, -math.pi / 2)
                    
    return circuit
