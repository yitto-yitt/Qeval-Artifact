# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    
    # In pyQPanda, we handle parameterized circuits differently
    # We'll create a template that can be used with different theta values
    def parametrized_circuit(theta_val):
        local_prog = pq.QProg()
        local_prog << pq.H(qubits[0])
        local_prog << pq.RZ(qubits[0], theta_val)
        return local_prog
    
    return parametrized_circuit

machine.finalize()
