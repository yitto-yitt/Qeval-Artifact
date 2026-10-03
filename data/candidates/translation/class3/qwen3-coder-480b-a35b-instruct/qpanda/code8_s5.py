# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(1)
    
    prog = pq.QProg()
    theta = pq.Parameter("theta")
    prog.insert(pq.RX(qubits[0], theta))
    
    if value is not None:
        prog = pq.bind_parameters(prog, {theta: value})
        return prog, machine, qubits
    
    return prog, machine, qubits
