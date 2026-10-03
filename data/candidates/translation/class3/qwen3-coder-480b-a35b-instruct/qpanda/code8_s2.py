# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    theta = pq.Parameter("theta")
    quantum_machine = pq.QMachine()
    qubits = quantum_machine.qAlloc_many(1)
    
    prog = pq.QProg()
    prog.insert(pq.RX(qubits[0], theta))
    
    if value is not None:
        # Bind the parameter to the specific value
        bound_prog = prog.bind_parameters({theta: value})
        return bound_prog
    return prog
