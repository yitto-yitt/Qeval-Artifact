# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_diagonal_circuit(diag):
    num_qubits = int(round(math.log2(len(diag))))
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    if hasattr(pq, 'DiagonalGate'):
        circuit = pq.DiagonalGate(qubits, diag)
    elif hasattr(pq, 'diagonal_gate'):
        circuit = pq.diagonal_gate(qubits, diag)
    else:
        raise AttributeError("Diagonal gate function not found in pyqpanda3.core")
        
    return circuit
