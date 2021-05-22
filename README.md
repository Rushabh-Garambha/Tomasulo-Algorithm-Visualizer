# Speculative Tomasulo Implementation

This is term project for CMSC-611 Advance Computer Architecture. This project generates a Tomasulo Algorithm Simulation Environment with GUI.

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyQT.

```bash
pip install PyQT
```

## Usage
To run the project, run the file tomasulo.py

```bash
python tomasulo.py
```

To change the program(set of instructions) that is ran in simulation, make changes in the Config.py file.

Description of variables that can be altered:

num_of_register : number of total registers in the system

instruction_win_size : size of the instruction window

rob_size: size of reorder buffer

functional_units : list of available functional units

## Supported instructions

```
ADD Dest, Source1, Source2    // Dest = Source1 + Source2
SUB Dest, Source1, Source2    // Dest = Source1 - Source2
MUL Dest, Source1, Source2    // Dest = Source1 * Source2
DIV Dest, Source1, Source2    // Dest = Source1 / Source2
LD  Dest, Source1, Source2    // Dest = Value 
BGE Source1, Source2, Location   // Branch to Location if Source1 greater than or equal to Source2
BNEZ Source1, Location   // Branch to location if Source1 not equal to zero
BEQZ Source1, Location   // Branch to location if Source1 equal to zero
```
