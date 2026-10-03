# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    
    # To prepare state |1>, we need to apply X gate to the last qubit (assuming little endian)
    # In pyqpanda, to prepare a specific computational basis state, we typically use X gates
    # For state |1> on n-qubit register means all qubits in |0> except last one in |1>
    # Actually, this means preparing the state where the binary representation is 1 (last qubit is 1, others are 0)
    prog << pq.X(qubits[num_qubits - 1])
    
    machine.finalize()
    return prog
