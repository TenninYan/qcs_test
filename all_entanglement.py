"""
Simple script to verify that the QMI is working.
After you have activated the virtual environment that comes with your QMI
(using source ~/.virtualenvs/venv/bin/activate), run this as:

    python hello_qmi.py [<qcname>]

Options:

    <qcname>        Name of a quantum computer available through the pyQuil API
                    [default: 9q-generic-qvm]

"""
import math

from pyquil import Program, get_qc
from pyquil.api import QVM
from pyquil.gates import RX, CNOT, MEASURE

import numpy as np

def hello_qmi(device_name: str = "9q-generic-qvm") -> None:
    """
    Get acquainted with your quantum computer by asking it to perform a simple
    coin-toss experiment. Involve 3 qubits in this experiment, and ask each one
    to give 10 results.

    :param device_name: The name of a quantum computer which can be retrieved
                        from `pyquil.api.get_qc()`. To find a list of all
                        devices, you can use `pyquil.api.list_devices()`.
    """
    # Initialize your Quil program
    program = Program()
    # Declare 3 bits of memory space for the readout results of all three qubits
    readout = program.declare('ro', 'BIT', 16)
    # For each qubit, apply a pulse to move the qubit's state halfway between
    # the 0 state and the 1 state
    program += RX(math.pi / 2, 1)

    program += CNOT(1,0) 
    program += CNOT(0,7) 
    program += CNOT(7,6) 
    program += CNOT(6,5) 

    program += CNOT(1,2) 
    program += CNOT(2,3) 
    program += CNOT(3,4) 

    program += CNOT(1,16) 
    program += CNOT(16,17) 
    program += CNOT(17,10) 
    program += CNOT(10,11) 

    program += CNOT(16,15) 
    program += CNOT(15,14) 
    program += CNOT(14,13) 
    program += CNOT(13,12) 

    # Add measurement instructions to measure the qubits and record the result
    # into the respective bit in the readout register
    program += MEASURE(0, readout[0])
    program += MEASURE(1, readout[1])
    program += MEASURE(2, readout[2])
    program += MEASURE(3, readout[3])
    program += MEASURE(4, readout[4])
    program += MEASURE(5, readout[5])
    program += MEASURE(6, readout[6])
    program += MEASURE(7, readout[7])

    program += MEASURE(10, readout[8])
    program += MEASURE(11, readout[9])
    program += MEASURE(12, readout[10])
    program += MEASURE(13, readout[11])
    program += MEASURE(14, readout[12])
    program += MEASURE(15, readout[13])
    program += MEASURE(16, readout[14])
    program += MEASURE(17, readout[15])

    # This tells the program how many times to run the above sequence
    program.wrap_in_numshots_loop(100)

    # Get the quantum computer we want to run our experiment on
    qc = get_qc(device_name, as_qvm=True)

    # Compile the program, specific to which quantum computer we are using
    compiled_program = qc.compile(program)

    # Run the program and get the 10 x 3 array of results
    results = np.array(qc.run(compiled_program))
    
    np.savetxt('entanglement.txt', results, fmt='%.0f')
    # Print the results. We expect to see 30 random 0's and 1's
    print(f"Your{' virtual' if isinstance(qc.qam, QVM) else ''} quantum "
          f"computer, {device_name}, greets you with:\n", results)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        hello_qmi(device_name=sys.argv[1].strip())
    else:
        hello_qmi()
