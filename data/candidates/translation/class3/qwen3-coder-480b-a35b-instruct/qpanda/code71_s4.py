# EVAL_META: task_id=71, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CU(3.14159/2, 0, 0, qubits[0], qubits[1]))  # CSX gate implemented as CU with pi/2 rotation
    prog.insert(pq.H(qubits[1]))
    
    return prog, qubits, machine
