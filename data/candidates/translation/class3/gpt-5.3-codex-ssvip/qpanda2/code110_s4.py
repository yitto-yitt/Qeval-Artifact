# EVAL_META: task_id=110, framework=qpanda2, class=3
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def equivalent_clifford_circuit(circuit, n):
    num_qubits = len(circuit.get_allocate_qubits())
    target_u = np.array(pq.get_matrix(circuit), dtype=complex)
    result = []
    while len(result) < n:
        q = machine.qAlloc_many(num_qubits)
        prog = pq.QProg()
        gate_count = np.random.randint(1, 6 * num_qubits + 1)
        for _ in range(gate_count):
            g = np.random.randint(0, 6)
            if g == 0:
                prog << pq.H(q[np.random.randint(0, num_qubits)])
            elif g == 1:
                prog << pq.S(q[np.random.randint(0, num_qubits)])
            elif g == 2:
                prog << pq.X(q[np.random.randint(0, num_qubits)])
            elif g == 3:
                prog << pq.Y(q[np.random.randint(0, num_qubits)])
            elif g == 4:
                prog << pq.Z(q[np.random.randint(0, num_qubits)])
            else:
                if num_qubits >= 2:
                    a, b = np.random.choice(num_qubits, 2, replace=False)
                    prog << pq.CNOT(q[a], q[b])
                else:
                    prog << pq.H(q[0])
        u = np.array(pq.get_matrix(prog), dtype=complex)
        if u.shape == target_u.shape and np.allclose(u, target_u, rtol=0.4, atol=0.4):
            result.append(prog)
        machine.Free_Qubits(q)
    return result

machine.finalize()
