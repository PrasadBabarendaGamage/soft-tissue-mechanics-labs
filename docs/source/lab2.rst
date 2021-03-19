
.. |vspace| raw:: latex

   \vspace{5mm}

.. _lab2:

*****************************
Lab 2: Stress transformations
*****************************

.. toctree::
   :maxdepth: 2

The objectives of this lab are to:

      1. transform 2nd Piola-Kirchhoff stress tensor components to Cauchy tensor components.

      2. transform stresses and strains between reference spatial and material (fibre) coordinates.

The deformations that will be considered in this lab include uniaxial deformation and equi-biaxial extension of a unit cube.

========
Revision
========

Before starting this lab, please be sure to have completed :ref:`Lab 1: Analysing deformation in isotropic materials <lab1>`.

===================================================================================
Section 1: Transforming from 2nd Piola-Kirchhoff to Cauchy stress tensor components
===================================================================================


1. Start OpenCMISS and load the "Kinematics analysis" project. Select "Model 1 (Uniaxial extension of unit cube)" from the drop down menu and click the "Run" button.

|vspace|

2. Open the simulation results pane and use the components of the 2nd Piola-Kirchhoff stress tensor :math:`(\boldsymbol{T})` and the deformation gradient tensor :math:`(\boldsymbol{F})` to determine the Cauchy components of the stress tensor :math:`(\boldsymbol{\Sigma})` (Don't forget the Jacobian :math:`(J)`). See :ref:`this link <opening_simulation_pane>` for an example on how to open the simulation results pane.

  .. Note::

      Hint: See equations in Section 3.1 of `Nash and Hunter (2007) <https://github.com/OpenCMISS-Examples/soft-tissue-mechanics-labs/releases/download/v2.0/chapter-heartmech_nash_hunter_2007_wspc_2up.pdf>`_.


|vspace|

3. Select "Problem" from the menu bar and repeat step 1-2 for the remaining models in the kinematics analysis project.

|vspace|

.. note::

    By the end of this section you should be able to:

    - derive the Cauchy stress tensor components from the second Piola-Kirchhoff stress tensor components using the deformation gradient tensor.


===================================================================
Section 2: Transforming stresses between rotated coordinate systems
===================================================================

Uniaxial extension of a unit cube
---------------------------------

1. Consider the uniaxial deformation shown in the figure below, where a set of material axes are aligned with the spatial reference axes. In the following figure, the gold arrows represent the first material axis (for example, this might be a the orientation of a collagen fibre within tissue):

  .. image:: images/uniaxial_0_degrees_fibres.png

  In the screenshot:
    - the undeformed (reference) configuration of the object (a unit cube) is shown in red;
    - the deformed (current) configuration of the object is shown in green; and
    - the gold arrows indicate the direction of the first material (fibre) axis in the object. In general, the microstructural fibres **are not necessarily parallel** to the direction of stretch or load.

  |vspace|

  This deformation is described by the following equations:

  .. math::

    x_1 = \frac{3}{2}X_1 ~~~~ x_2 = \sqrt{\frac{2}{3}}X_2 ~~~~ x_3 = \sqrt{\frac{2}{3}}X_3

  .. note::

  In all figures, :math:`x` represents :math:`X_1` and :math:`x_1`, :math:`y` represents :math:`X_2` and :math:`x_2`, and :math:`z` represents :math:`X_3` and :math:`x_3`. 

|vspace|

2. Write down (see :ref:`Lab 1 <lab1>`):

  - the deformation gradient tensor, :math:`\boldsymbol{F}=\frac{\partial\boldsymbol{x}}{\partial\boldsymbol{X}}`
  - the right Cauchy-Green deformation tensor, :math:`\boldsymbol{C}` and
  - the Green-Lagrange strain tensor. Label this as :math:`\boldsymbol{E}_{ref}` (to indicate that it is defined with respect to the reference spatial coordinates).

  .. Note::

      This is the same deformation used in Model 1 in :ref:`Lab 1 <lab1>`, so you should not need to re-do these calculations.

      For this particular model, the second Piola-Kirchhoff stress tensors with respect to both the reference spatial, and material fibre axes, are:

      .. math::

        \boldsymbol{T_{ref}} = \boldsymbol{T_{fib}} = 
        \begin{bmatrix}
          440.5  & 0       & 0 \\
          0      & 0       & 0 \\
          0      & 0       & 0
        \end{bmatrix}

      (**Note:** While the uniaxial deformation in Model 1 of :ref:`Lab 1 <lab1>` is the same as that considered here, the **stress tensors are different between thse two labs** because different stress-strain constitutive relations have been used - this difference will be covered in :ref:`Lab 3 <lab3>`).

|vspace|

.. _tensor_transformations:

Uniaxial deformation with respect to rotated material axes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3. Now consider the same deformation, except that the material fibre axes are no longer aligned with the reference spatial axes. They are now rotated anti-clockwise by an angle of :math:`\theta=30` degrees from the :math:`X_{1}` axis (in the :math:`X_{1}`-:math:`X_{2}` plane), as shown in the figure below.

  .. image:: images/uniaxial_30_degrees_fibres.png

|vspace|

  For the following exercises, you are asked to transform strain and stress tensors between the reference spatial coordinates and the material fibre coordinate systems using the generalised rotational transform given by:

  .. math::

    \boldsymbol{E}_{fib} = \boldsymbol{Q}^{T} \boldsymbol{E}_{ref} \boldsymbol{Q}

  where :math:`\boldsymbol{E}_{ref}` and :math:`\boldsymbol{E}_{fib}` are  Green-Lagrange strain tensors defined with respect to the reference spatial and material fibre axes, respectively, and :math:`\boldsymbol{Q}` is the orthogonal rotation matrix, which for this example is defined by:

  .. math::

      \boldsymbol{Q} = 
      \begin{bmatrix}
        \cos(\theta) & -\sin(\theta) & 0  \\
        \sin(\theta) &  \cos(\theta) & 0  \\
        0              &  0              & 1
      \end{bmatrix}

|vspace|

4. Calculate the components of the Green-Lagrange strain tensor with respect to the material fibre axes (:math:`\boldsymbol{E}_{fib}`) via the appropriate tensor transformation (see Step 3).

|vspace|

5. Explain similarities/differences between :math:`\boldsymbol{E}_{fib}` and :math:`\boldsymbol{E}_{ref}` for this model.

|vspace|

6. The relationship between second Piola-Kirchhoff stress tensors defined with respect to reference spatial and material fibre coordinates is (note the similarity to Step 3):

  .. math::

    \boldsymbol{T}_{fib} = \boldsymbol{Q}^{T} \boldsymbol{T}_{ref} \boldsymbol{Q}

  Invert this equation, and then calculate the second Piola-Kirchhoff stress components with respect to the reference spatial axes (:math:`\boldsymbol{T}_{ref}`) from the following components of the second Piola-Kirchhoff stress tensor with respect to the material fibre axes (:math:`\boldsymbol{T}_{fib}`):

  .. math::

    \boldsymbol{T_{fib}} = 
    \begin{bmatrix}
      330.345   & -190.725  & 0 \\
      -190.725  & 110.115   & 0 \\
      0       & 0       & 0
    \end{bmatrix}

|vspace|

7. Explain similarities/differences between :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}` for this model.

|vspace|

8. What would you expect from the analysis in steps 4-7 if the fibre angle was changed from :math:`\theta=30` degrees to :math:`\theta=45` degrees, or to :math:`\theta=90` degrees for this model?  Explain the differences/similarities of the stress tensors :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}` for this uniaxial deformation model.

  .. note::

    You should not need to do any calculations to answer this questions, but if you would like the extra practice, perform steps 4-7 using:

    :math:`\theta=45` degrees, where the second Piola-Kirchhoff stress tensor with respect to the material fibre axes is:

      .. math::

        \boldsymbol{T_{fib}} = 
        \begin{bmatrix}
          220.2   & -220.2  & 0 \\
          -220.2  & 220.2   & 0 \\
          0       & 0       & 0
        \end{bmatrix}

    and/or :math:`\theta=90` degrees, where the second Piola-Kirchhoff stress tensor with respect to the material fibre axes is:

      .. math::

        \boldsymbol{T_{fib}} = 
        \begin{bmatrix}
          0      & 0       & 0 \\
          0      & 440.5   & 0 \\
          0      & 0       & 0
        \end{bmatrix}

|vspace|

Here are the :ref:`solutions to Steps 1-8<lab2_section2_step8_solutions>`.


.. _isotropic_biaxial_extension_of_unit_cube:

Equi-biaxial extension of a unit cube
-------------------------------------

9. Start OpenCMISS and load the stress analysis project (described in the :ref:`Starting OpenCMISS <starting-OpenCMISS>` section).

|vspace|

10. Select "Model 1 (Equi-biaxial extension of unit cube, 0 degree fibre rotation)" from the drop down menu and click the "Run" button (screenshots of this procedure are shown in the :ref:`Running models in OpenCMISS <running-models-in-OpenCMISS>` section).

|vspace|

11. After a short time, the model should have solved and the simulation results will appear in the 3D graphics window as shown in the screenshot below.

  .. image:: images/lab2_model1.png

  |vspace|

  In this graphical window:

      - the undeformed (reference) configuration of the unit cube is shown in red, and
      - the deformed (current) configuration is shown in green (:math:`x_{1}`, :math:`x_{2}`, :math:`x_{3}` components of the deformed coordinates are shown at the corners of the model.
      - ignore the gold arrows for now - these will be needed later.

  The model in the 3D graphics window can be rotated (click-drag-left-mouse button), translated (click-drag-middle-mouse button), or zoomed (click-drag-middle-mouse button).

|vspace|


12. This equi-biaxial deformation is incompressible (i.e. maintains constant volume) described by the equations:

  .. math::

    x_1 = \frac{5}{4}X_1 ~~~~ x_2 = \frac{5}{4}X_2 ~~~~ x_3 = \frac{16}{25}X_3

|vspace|

13. Write down:

  - the deformation gradient tensor (:math:`\boldsymbol{F}=\frac{\partial\boldsymbol{x}}{\partial\boldsymbol{X}}`),
  - the right Cauchy-Green deformation tensor (:math:`\boldsymbol{C}`), and
  - Green-Lagrange strain tensor (:math:`\boldsymbol{E}`) (label this :math:`\boldsymbol{E}_{ref}`).

  .. Note::

      This is the same deformation used in Model 2 of Lab 1, so you should not need to re-do these calculations.

|vspace|

Equi-biaxial deformation with respect to rotated material fibre axes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

14. Return to the model selection drop down menu and select/run "Model 3 (Equi-biaxial extension of unit cube, 30 degree fibre rotation)". This model is similar to the previous models, except that the material fibre axes are no longer aligned with the reference (spatial) axes. For this model, the material fibre axis is rotated anti-clockwise by an angle of :math:`\theta=30` degrees from the :math:`X_{1}` axis (in the :math:`X_{1}`-:math:`X_{2}` plane). When visualising these models, the gold arrows in the graphics window indicate the direction of the first material fibre axis (along which the first material coordinate is defined), and the second material fibre axis (not shown) is perpendicular to the gold arrow but lies within :math:`X_{1}`-:math:`X_{2}` plane.

|vspace|

15. Determine the Green-Lagrange strain tensor components with respect to the material fibre axes (:math:`\boldsymbol{E}_{fib}`) using the approach in Section 2.

|vspace|

16. Check your answers to Step 15 against the simulation results from OpenCMISS.

  .. Note::

      Drag the right edge of the 3D graphics window to reveal the stress and strain tensor components associated with the simulation in material fibre and reference spatial coordinates. See :ref:`this link <opening_simulation_pane>` for an example on how to open this pane.

|vspace|

17. Explain similarities/differences between :math:`\boldsymbol{E}_{fib}` and :math:`\boldsymbol{E}_{ref}` for this model.

|vspace|

18. From the solution output, write down  :math:`\boldsymbol{T}_{fib}` (the second Piola-Kirchhoff stress tensor with respect to the material fibre axes). Use this to determine the second Piola-Kirchhoff stress components with respect to the reference spatial coordinate axes (:math:`\boldsymbol{T}_{ref}`) via the approach Section 2.

|vspace|

19. Check your answers to Step 18 against the simulation results.

|vspace|

20. Explain similarities/differences between :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}` for this model.

|vspace|

21. What would you expect from the analysis in steps 15-20 if the fibre angle was changed from :math:`\theta=30` degrees to :math:`\theta=45` degrees, or to :math:`\theta=90` degrees for this equi-biaxial deformation model?  Explain the differences/similarities between the two strain tensors for this model.  Then explain the differences/similarities between the two stress tensors for this model.

  .. note::

    You should not need to do any calculations to answer this questions. It is fine to do so if you would like some extra practice - just perform steps 15-20 with :math:`\theta=45` degrees by selecting the Model 4 then Model 6 from the "Run" menu.

|vspace|

Here are the :ref:`solutions to Step 21 <lab2_section2_step21_solutions>`.


Questions to think about:
-------------------------

After you have completed the exercises above, consider the following questions:

a. How do changes in :math:`\boldsymbol{E}_{ref}` for different fibre angles (:math:`\theta`) in the equi-biaxial deformation compare with the changes seen in the uniaxial deformation.

b. How do changes in :math:`\boldsymbol{E}_{fib}` for different fibre angles (:math:`\theta`) in the equi-biaxial deformation compare with the changes seen in the uniaxial deformation.

c. How do changes in :math:`\boldsymbol{T}_{ref}` for different fibre angles (:math:`\theta`) in the equi-biaxial deformation compare with the changes seen in the uniaxial deformation.

d. How do changes in :math:`\boldsymbol{T}_{fib}` for different fibre angles (:math:`\theta`) in the equi-biaxial deformation compare with the changes seen in the uniaxial deformation.

e. Will the invariants of :math:`\boldsymbol{C}` be the same or different when calculated with respect to reference spatial or material fibre coordinates?

|vspace|

.. note::

  By completing this lab, you should be able to:

    - convert between 2nd Piola-Kirchhoff and Cauchy stress tensors.

    - analyse large deformation kinematics with respect to reference spatial or rotated material fibre coordinates, and convert between them.

    - analyse stress tensors with respect to reference spatial or rotated material fibre coordinates, and convert between them.


