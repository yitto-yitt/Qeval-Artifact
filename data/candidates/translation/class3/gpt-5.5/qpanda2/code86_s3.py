# EVAL_META: task_id=86, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def collect_linear_blocks_with_and_without_limit():
    full_linear_block = pq.QCircuit()
    full_linear_block.insert(pq.CNOT(qubits[0], qubits[1]))
    full_linear_block.insert(pq.CNOT(qubits[1], qubits[2]))
    full_linear_block.insert(pq.CNOT(qubits[2], qubits[3]))
    full_linear_block.insert(pq.CNOT(qubits[3], qubits[4]))

    full_block = pq.QCircuit()
    full_block.insert(pq.H(qubits[0]))
    full_block.insert(full_linear_block)

    limited_linear_block_1 = pq.QCircuit()
    limited_linear_block_1.insert(pq.CNOT(qubits[0], qubits[1]))
    limited_linear_block_1.insert(pq.CNOT(qubits[1], qubits[2]))

    limited_linear_block_2 = pq.QCircuit()
    limited_linear_block_2.insert(pq.CNOT(qubits[2], qubits[3]))
    limited_linear_block_2.insert(pq.CNOT(qubits[3], qubits[4]))

    limited_block = pq.QCircuit()
    limited_block.insert(pq.H(qubits[0]))
    limited_block.insert(limited_linear_block_1)
    limited_block.insert(limited_linear_block_2)

    return full_block, limited_block
