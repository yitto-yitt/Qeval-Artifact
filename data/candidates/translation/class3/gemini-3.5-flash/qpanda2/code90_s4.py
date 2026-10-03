# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = pq.QCircuit()
    circuit << pq.X(q[1]) << pq.H(q[2])
    
    control_qubits = pq.QVec()
    control_qubits.append(q[0])
    control_qubits.append(q[3])
    
    controlled_circuit = circuit.control(control_qubits)
    
    prog = pq.QProg()
    prog << controlled_circuit
    return prog

machine.finalize()
