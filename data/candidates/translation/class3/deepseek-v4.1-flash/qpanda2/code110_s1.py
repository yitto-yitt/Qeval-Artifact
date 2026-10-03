# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def equivalent_clifford_circuit(circuit, n):
    qubits = circuit.get_qubits()
    num_qubits = len(qubits)
    result = []
    for _ in range(n):
        qc = QCircuit()
        qc << circuit
        length = random.randint(5, 20)
        gates = []
        for _ in range(length):
            if num_qubits == 1:
                gate = random.choice(['H', 'X', 'Y', 'Z'])
                gates.append((gate, qubits[0]))
            else:
                if random.random() < 0.5:
                    gates.append(('H', random.choice(qubits)))
                else:
                    ctrl = random.choice(qubits)
                    targ = random.choice(qubits)
                    while targ == ctrl:
                        targ = random.choice(qubits)
                    gates.append(('CNOT', ctrl, targ))
        for g in gates:
            if g[0] == 'H':
                qc << H(g[1])
            elif g[0] == 'X':
                qc << X(g[1])
            elif g[0] == 'Y':
                qc << Y(g[1])
            elif g[0] == 'Z':
                qc << Z(g[1])
            else:
                qc << CNOT(g[1], g[2])
        for g in reversed(gates):
            if g[0] == 'H':
                qc << H(g[1])
            elif g[0] == 'X':
                qc << X(g[1])
            elif g[0] == 'Y':
                qc << Y(g[1])
            elif g[0] == 'Z':
                qc << Z(g[1])
            else:
                qc << CNOT(g[1], g[2])
        result.append(qc)
    return result

if __name__ == '__main__':
    machine.finalize()
