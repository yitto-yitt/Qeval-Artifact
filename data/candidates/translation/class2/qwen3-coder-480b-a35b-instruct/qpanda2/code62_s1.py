# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    circuit = pq.QCircuit()
    
    for i in range(len(basis)):
        if state[i] == 1:
            circuit.insert(pq.X(qubits[i]))
        if basis[i] == 1:
            circuit.insert(pq.H(qubits[i]))
    
    prog = pq.QProg()
    prog.insert(circuit)
    
    return prog
