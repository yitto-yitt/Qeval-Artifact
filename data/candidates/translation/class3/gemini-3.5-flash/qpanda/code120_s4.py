# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(num_qubits)
    
    circuit = pq.QCircuit()
    complex_diag = [complex(x) for x in diag]
    circuit << pq.DiagonalGate(qubits, complex_diag)
    
    # Keep the machine alive by attaching it to the circuit object
    circuit._machine = machine
    return circuit
