# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def rx_gate(value=None):
    qubits = machine.qAlloc_many(1)
    prog = pq.QProg()
    
    if value is not None:
        prog << pq.RX(qubits[0], value)
        return prog, qubits
    else:
        # In pyQPanda, we need to handle parametrized gates differently
        # Since pyQPanda doesn't have the same parameter system as Qiskit,
        # we return a function that can accept the parameter later
        def create_rx_prog(param_value):
            local_prog = pq.QProg()
            local_prog << pq.RX(qubits[0], param_value)
            return local_prog, qubits
        return create_rx_prog, qubits

machine.finalize()
