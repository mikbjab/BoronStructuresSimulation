<h1 align="center">Boron Planar Structures simulation</h1>

<p align="center">
This project is an attempt to simulate the evolution of boron planar structure using evolutionary approach.
It simulates with promising result structures with fitting function dependent only on neighbours of each atom.
Right now I'm trying to fit parameters of the spring model so that the simulation using this fitting function generate similar result to the first one.
</p>
<h2 align="left">Structure of the project</h2>
<p>
  I try to keep different functionalities seperately to make it easier to make changes in different modules, without ruining rest of the functions.

  In package "util" are defined functions which are used in different simulation: fittingFunctions.py (fitting function with energy table, and fitting function for spring model),
  Grid.py (class Grid which holds positions of the boron atoms), GridFactory.py (static class used for producing Grid objects), viewGrid.py (functions for viewing Grid object using matplotlib).

  In package "fitParameters" are defined functions used in fitting spring model to previous fit function and in simulating grid evolution: fit_structures.py (functions for evolution of grid, generating random grids, fitting parameters of spring model), test_structures.py (code for testing parameters on test set), train_least_square.py (code for fitting parameters using least squares method), train_walk_selected_random.py (code for fitting using random walk with training set partially randomly generated and partially manually chosen).

  Directory resources contains training sets ("training", "training_selected"), test set ("test") and fitted parameters.
</p>
<h2 align="left">
  Neighbours-dependent fitting function
</h2>
<p align="left">
  
  <table align="center">
<thead>
  <tr>
    <th>$n$</th>
    <th>$E_n$</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>$0$</td>
    <td>$0$</td>
  </tr>
  <tr>
    <td>$1$</td>
    <td>$1.7803$</td>
  </tr>
  <tr>
    <td>$2$</td>
    <td>$5.1787$</td>
  </tr>
  <tr>
    <td>$3$</td>
    <td>$5.6504$</td>
  </tr>
  <tr>
    <td>$4$</td>
    <td>$6.2522$</td>
  </tr>
  <tr>
    <td>$5$</td>
    <td>$6.5718$</td>
  </tr>
  <tr>
    <td>$6$</td>
    <td>$6.5116$</td>
  </tr>
</tbody>
</table>
</p>
