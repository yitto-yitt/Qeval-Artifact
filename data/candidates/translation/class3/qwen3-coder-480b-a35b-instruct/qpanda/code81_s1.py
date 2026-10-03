# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda import *

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""
    
    # Create a quantum machine
    machine = init(QMachineType.CPU)
    
    # Convert QASM string to quantum circuit
    prog = convert_qasm_to_qprog(qasm_string, machine)
    
    # Get the quantum circuit
    qc = prog.get_qgate_num()
    
    # Finalize the machine
    finalize()
    
    return prog
