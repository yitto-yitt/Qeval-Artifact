# EVAL_META: task_id=147, framework=qpanda, class=3
import pyqpanda3.core as pq

def mcy(qc):
    # Get the qubits from the circuit
    qubits = qc.qubits()
    
    # Apply multi-controlled Y gate using X gate conjugated with S gates
    # Since pyQPanda doesn't have direct MCY, we use MCX with S† and S gates
    qc.s(qubits[4])  # Apply S gate to target qubit
    qc.controlled_by([qubits[0], qubits[1], qubits[2], qubits[3]]).x(qubits[4])
    qc.s_dagger(qubits[4])  # Apply S† gate to target qubit
    
    return qc
