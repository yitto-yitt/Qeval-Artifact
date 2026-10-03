# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import math

def bell_each_shot():
    # Initialize quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    # Create quantum program
    prog = pq.QProg()
    
    # Apply gates: H on qubit 0, then CNOT from qubit 0 to qubit 1
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    
    # Measure all qubits
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    prog.insert(pq.Measure(qubits[1], cbits[1]))

    # Run the program with 10 shots
    result = machine.run_with_configuration(prog, cbits, 10)
    
    # Calculate total shots
    import builtins
    total = builtins.sum(result.values())
    
    # Return probability distribution
    return {key: value / total for key, value in result.items()}
