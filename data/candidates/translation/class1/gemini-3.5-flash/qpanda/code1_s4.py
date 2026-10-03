# EVAL_META: task_id=1, framework=qpanda, class=1
import pyqpanda3.core as pq

def run_bell_state_simulator():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.Measure(qubits[0], cbits[0]) \
         << pq.Measure(qubits[1], cbits[1])
         
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
