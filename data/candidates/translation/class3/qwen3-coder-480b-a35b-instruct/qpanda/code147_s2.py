# EVAL_META: task_id=147, framework=qpanda, class=3
import pyqpanda3.core as pq

def mcy(qc):
    # Get the qubits from the circuit
    qubits = qc.qubits()
    
    # Create a multi-controlled Y gate using X gate conjugated with S gates
    # Since pyQPanda doesn't have direct MCY, we use MCX with S† and S gates
    # Y = S† X S, so for multi-controlled Y, we need S† on target, then MCX, then S on target
    
    # Apply S† to target qubit (qubit 4)
    qc.rz(qubits[4], -pq.PI/2)
    # Apply H to target qubit 
    qc.h(qubits[4])
    # Apply multi-controlled X with qubits 0,1,2,3 as controls and 4 as target
    qc.mcx([qubits[0], qubits[1], qubits[2], qubits[3]], qubits[4])
    # Apply H to target qubit again
    qc.h(qubits[4])
    # Apply S to target qubit
    qc.rz(qubits[4], pq.PI/2)
    
    return qc
