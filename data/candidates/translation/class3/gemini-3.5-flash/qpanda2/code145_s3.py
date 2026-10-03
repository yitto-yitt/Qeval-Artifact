# EVAL_META: task_id=145, framework=qpanda2, class=3
import pyqpanda as pq
import atexit

# Initialize global QVM and qubits
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(30)

# Register manual cleanup
atexit.register(machine.finalize)

def qft_inverse(n):
    if n <= 0:
        return pq.QCircuit()
    qubits = [global_qubits[i] for i in range(n)]
    qft_circ = pq.QFT(qubits)
    return qft_circ.dagger()
