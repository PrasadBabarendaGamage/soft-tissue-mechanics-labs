
.. |vspace| raw:: latex

   \vspace{5mm}

.. _lab1:

***************************************************
Lab 1: Analysing deformation in isotropic materials
***************************************************

.. toctree::
   :maxdepth: 2

The objective of this lab is to analyse large deformation kinematics with respect to reference coordinates in isotropic materials, for with the stiffness properties are the same in all directions. The deformations you will be analysing include:

  - Model 1 (Uniaxial extension of unit cube)
  - Model 2 (Equibiaxial extension of unit cube)
  - Model 3 (Simple shear of unit cube)
  - Model 4 (Shear of unit cube)
  - Model 5 (Extension and shear of unit cube)

Before starting this lab, please read the :ref:`Using OpenCMISS <using-opencmiss>` section to familiarise yourself with the software used in this lab.

|vspace|

===================================
Section 1: Solving mechanics models
===================================

1. Start OpenCMISS and load the "Kinematics analysis" project (described in the :ref:`Starting OpenCMISS <starting-OpenCMISS>` section).

|vspace|

2. Select "Model 1 (uniaxial extension of unit cube)" from the drop down menu and click the "Run" button (screenshots of this procedure are shown in the :ref:`Running models in OpenCMISS <running-models-in-OpenCMISS>` section).

|vspace|

3. After a short time, the model should have solved and the simulation results pane will open, as shown in the screenshot below.

  .. image:: images/lab1_model1.png

  |vspace|

  The simulation results are shown in the 3D graphics window. In this graphical window:

      - the undeformed (reference) configuration of the unit cube is shown in red; and
      - the deformed (current) configuration is shown in green (:math:`x_{1}`, :math:`x_{2}`, :math:`x_{3}` components of the deformed coordinates are shown at the corners of the model).

  The model in the 3D graphics window can be rotated (click-drag-left-mouse button), translated (click-drag-middle-mouse button), or zoomed (click-drag-right-mouse button).

|vspace|

==========================
Section 2: Strain analysis
==========================

4. Write down the coordinate equations that describe this deformation in the form :math:`\boldsymbol{x}=f(\boldsymbol{X})`, i.e.:

  .. math::

    x_1 = aX_1 + bX_2 + cX_3\\
    x_2 = dX_1 + eX_2 + fX_3\\
    x_3 = gX_1 + hX_2 + iX_3

  where the constants :math:`a` to :math:`i` need to be identified from the undeformed and deformed coordinates of the model shown in the graphics window.

.. note::

   The undeformed (reference) configuration is the unit cube shown in red.

|vspace|

5. Determine the deformation gradient tensor :math:`(\boldsymbol{F}=\frac{\partial\boldsymbol{x}}{\partial\boldsymbol{X}})`.

|vspace|

6. Evaluate the determinant of :math:`\boldsymbol{F}` to see whether the material is incompressible (i.e. maintains constant volume).

|vspace|

7. Determine:

  - right Cauchy-Green deformation tensor :math:`(\boldsymbol{C})`,
  - :math:`I_1=trace(\boldsymbol{C})`,
  - :math:`I_3=det(\boldsymbol{C})`, and the
  - Green-Lagrange strain tensor :math:`(\boldsymbol{E})`.

|vspace|

8. Check your answers to 5-7 against the simulation results.

  .. _opening_simulation_pane:

  .. Note::

      Click and drag on the right hand boundary of the 3D graphics window to view the simulation results as shown in the screenshots below:

      .. image:: images/showing_simulation_results1.png

      .. image:: images/showing_simulation_results2.png

  .. Note::

      In some cases, an apparent zero may be preceded by a negative sign. This value should still be treated as zero (i.e. ignore the negative sign).

|vspace|

9. Select "Problem" from the menu bar and repeat steps 2-8 for the remaining models in the kinematics analysis project:

    - Model 2 (Equibiaxial extension of unit cube)
    - Model 3 (Simple shear of unit cube)
    - Model 4 (Shear of unit cube)
    - Model 5 (Extension and shear of unit cube)

|vspace|


Questions to consider
---------------------

After you have completed the above exercises, consider the following questions: 

a. What do the off-diagonal components of :math:`\boldsymbol{F}` represent?

|vspace|

b. In Model 1, why are :math:`E_{22}` and :math:`E_{33}` negative?  What does this represent?

|vspace|

c. In Model 4, what does the equality of :math:`F_{11}` and :math:`F_{33}` represent? Why is :math:`F_{22}` less than 1.

|vspace|

.. note::

  By the end of this lab you should be able to:

    - analyse large deformation kinematics with respect to reference coordinates, i.e. by determining :math:`\boldsymbol{F}`, :math:`\boldsymbol{C}`, invariants of :math:`\boldsymbol{C}`, and :math:`\boldsymbol{E}`.

    - relate the components of the deformation gradient tensor to the underlying deformation.

    - determine if a deformation is incompressible.

