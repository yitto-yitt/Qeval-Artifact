# EVAL_META: task_id=125, framework=qpanda, class=3
import pyqpanda3 as pq


def circ_to_gate(circ):
    # In pyQPanda3, we can wrap a quantum circuit as a gate using QProg
    # Create a new quantum program
    prog = pq.QProg()
    
    # Get quantum and classical registers from the input circuit
    qubits = circ.qubits
    cbits = circ.clbits
    
    # Append the circuit operations to the program
    prog.insert(circ)
    
    # Return the program which represents the gate equivalent
    return prog
