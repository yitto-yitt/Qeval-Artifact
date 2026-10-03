# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3.core as pq


def initialize_cnot_dihedral():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.T(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    # Since pyQPanda3 doesn't have a direct equivalent to Qiskit's CNOTDihedral,
    # we return the program which represents the circuit
    return prog
