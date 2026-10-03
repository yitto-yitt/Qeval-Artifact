# EVAL_META: task_id=71, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    sx = pq.RX(qubits[1], 3.141592653589793 / 2)
    sx.set_control([qubits[0]])
    prog << sx
    prog << pq.H(qubits[1])
    return prog

if __name__ == "__main__":
    circuit = create_quantum_circuit_based_h0_csx01_h1()
    print(circuit)
    machine.finalize()
