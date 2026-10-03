# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    # Convert the input circuit to pyQPanda format if needed
    # Assuming circuit is already in pyQPanda format or can be processed
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Get the state vector from the quantum program
    statevector = qvm.get_state_vector(circuit)
    qvm.finalize()
    
    return statevector
