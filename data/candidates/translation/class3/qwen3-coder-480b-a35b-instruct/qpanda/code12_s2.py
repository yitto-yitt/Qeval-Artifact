# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq


def get_unitary():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    unitary = pq.get_unitary(prog, qubits)
    pq.destroy_quantum_machine(machine)
    
    return unitary
