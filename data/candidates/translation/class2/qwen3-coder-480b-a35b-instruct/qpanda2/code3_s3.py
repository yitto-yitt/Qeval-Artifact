# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    prog = pq.QProg()
    
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.CNOT(qubits[0], qubits[2])
    
    # Add measurement
    cbits = machine.cAlloc_many(3)
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
    
    if drawing:
        # pyqpanda doesn't have built-in drawing like Qiskit
        # Return the program and None for drawing
        return prog, None
    
    machine.directly_run(prog)
    result = machine.get_q_result()
    machine.finalize()
    
    return prog
