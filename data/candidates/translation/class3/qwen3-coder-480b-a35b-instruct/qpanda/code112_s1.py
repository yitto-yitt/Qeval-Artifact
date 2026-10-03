# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda import *
from pyqpanda.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(len(pauli_strings[0]))
    cbits = machine.cAlloc_many(len(pauli_strings[0]))
    
    for pauli_string, time in zip(pauli_strings, times):
        hamiltonian = PauliOperator(pauli_string, 1.0)
        evolution_op = exp(hamiltonian * (-1j * time))
        
        for _ in range(reps):
            prog.insert(evolution_op.to_instruction(qubits))
            
    return prog
