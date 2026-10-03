# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    prog = pq.QProg()
    theta = pq.Parameter("theta")
    prog.insert(pq.RX(qubits[0], theta))
    
    if value is not None:
        prog = prog.parameterized_circuit({theta: value})
        machine.run(prog)
        return prog
    
    return prog

machine.finalize()
