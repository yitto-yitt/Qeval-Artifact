# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    circ = pq.QCircuit()
    h_gate = pq.H(qubits[2])
    c_h_gate = h_gate.control([qubits[0], qubits[1]])
    circ << c_h_gate
    return circ

prog = pq.QProg()
prog << create_controlled_hgate()
machine.directly_run(prog)
machine.finalize()
