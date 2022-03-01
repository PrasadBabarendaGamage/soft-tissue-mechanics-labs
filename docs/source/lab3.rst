
.. |vspace| raw:: latex

   \vspace{5mm}

.. _lab3:

**************************************************
Lab 3: Analysing stresses in anisotropic materials
**************************************************

.. toctree::
   :maxdepth: 2

The objective of this lab is to learn how to analyse anisotropic constitutive equations and stresses defined with respect to a material coordinate system.

========
Revision
========
Before starting this lab, please be sure to have completed:
  a. :ref:`Lab 1: Analysing deformation in isotropic materials <lab1>`, and
  b. :ref:`Lab 2: Stress transformations <lab2>`.

Section 2 of :ref:`Lab 2<lab2>` demonstrated how rotating the material-fibre axis with respect to the reference axes influences the components of the stress tensor.  For the model in :ref:`Section 2 of Lab 2 <isotropic_biaxial_extension_of_unit_cube>`, which considers an **isotropic cube subject to equi-biaxial deformation**, remind yourself:

  - What happened to the components of the stress tensor as the material-fibre axis was rotated? Why?
  
All of the analyses in the present lab will be based on the equi-biaxial deformation described in :ref:`Section 2 of Lab 2 <isotropic_biaxial_extension_of_unit_cube>`. The difference here is that we will now consider **anisotropic** mechanical properties that describe different stress-strain response alonf the different material axes.

===================================================
Section 1: Deriving components of the stress tensor
===================================================

1. Consider the following exponential constitutive relation, which is used to describe the **distortional** mechanical response of the cube considered in this lab:

  .. math::

    W_{I} = \frac{c_{1}}{2}(e^{Q}-1)

  where

  .. math::

    Q = & c_{ff}E^{2}_{ff} +
          c_{ss}E^{2}_{ss} + 
          c_{nn}E^{2}_{nn} + \\
        & 2c_{fs}(\frac{1}{2}(E_{fs}+E_{sf}))^{2} + 
          2c_{fn}(\frac{1}{2}(E_{fn}+E_{nf}))^{2} + 
          2c_{ns}(\frac{1}{2}(E_{ns}+E_{sn}))^{2}

Differentiate this strain energy density function with respect to each of the nine Green-Lagrange strain components (:math:`E_{\alpha \beta}`), where :math:`\alpha` and :math:`\beta` each represent one of the microstructural material coordinates, (:math:`f,s,n`). Thus, derive generalised analytical expressions for the nine **distortional components of the second Piola-Kirchhoff stress tensor** in terms of the strain components and the material constants: :math:`c_1, c_{ff}, c_{ss}, c_{nn}, c_{fs}, c_{fn}, c_{ns}`.

  .. Note::

      - At this stage, do not substitute any values for the strain components nor constants.
      
      - Recognising the similarity of terms should simplify this task.
      
      - Don't forget the chain rule when differentiating the exponential.

|vspace|

=============================================================
Section 2: Analysing stresses during equi-biaxial deformation
=============================================================

Analysing stresses with respect to the reference coordinates
------------------------------------------------------------

2. Using OpenCMISS, load the stress analysis project and run Model 1. (The procedure for running this simulation in OpenCMISS is outlined in :ref:`steps 1-3 in Section 2 of Lab 2 <isotropic_biaxial_extension_of_unit_cube>`). See :ref:`this link <opening_simulation_pane>` for an example on how to open the simulation results pane.

|vspace|

3. The Model 1 simulation uses the above constitutive equation with the following material constants:

  .. math::

    c_{1} &= 0.0475~kPa \\
    c_{ff} = c_{ss} = c_{nn} &= c_{fs} = c_{fn} = c_{ns} = 15.25 \\

  Substitute the Green-Lagrange strain components (:math:`\boldsymbol{E}_{ref}`) for this equi-biaxial deformation into your analytical expressions from Step 1 of this lab to determine values for the **distortional components of the second Piola-Kirchhoff stress tensor**. Verify that these distortional stresses are:

  .. math::

    T_{ref}^{ff\_dist} = T_{ref}^{ss\_dist} = 8.59~kPa

  .. Note::

      - Hint: in the steps below, you will use your your analytical equations from step 1 repeatedly to do number of calculations (with different parameters), so you might consider encoding your equations using a high level programming language (python, C, Matlab, etc) or a spreadsheet.

      - Hint: :math:`Q=3.74`.

      - Your calculations for :math:`T_{ref}^{ff\_dist}` and :math:`T_{ref}^{ss\_dist}` could be within :math:`{\pm}0.02~kPa` of the solution stated above due to round off errors.

      - These **distortional components of the second Piola-Kirchhoff stress tensor** (e.g. :math:`T_{ref}^{ff\_dist}`) do not match the stress values shown in the OpenCMISS results panel because the OpenCMISS results show only the **total stress components**, which will be considered in the following steps.

|vspace|

4. Now assume that the material is incompressible, and write down analytical expressions for the **total stress components** with respect to the reference coordinates: :math:`T_{ref}^{ff}` and :math:`T_{ref}^{ss}` (these are shown as :math:`T^{ff}` and :math:`T^{ss}` in Eqn 38 of `Nash and Hunter (2007) <https://github.com/OpenCMISS-Examples/soft-tissue-mechanics-labs/releases/download/v2.0/chapter-heartmech_nash_hunter_2007_wspc_2up.pdf>`_, or Eqn 15 of `Nash and Hunter (2000) <http://link.springer.com/article/10.1023%2FA%3A1011084330767>`_).

|vspace|

5. Calculate the **total stress components** with respect to the reference coordinates: :math:`T_{ref}^{ff}` and :math:`T_{ref}^{ss}` using the expressions you wrote down in Step 4 above. This requires addition of a dilatational component of stress called the **hydrostatic pressure**, :math:`p`, which is a scalar variable with a value that is provided in the simulation results. Check your total stress values against those in the simulation results.

  .. Note::

      - :math:`\{C^{MN}\}` is the **inverse** of :math:`\{C_{MN}\}`. (They are different tensors)

      - It is straightforward to invert a diagonal tensor. Check that :math:`\{C_{MN}\}^{-1}\{C_{MN}\}=\boldsymbol{I}`.

|vspace|

6. Using this analysis, what can you infer about the material symmetry of Model 1? Explain your observation. 

|vspace|

|vspace|

7. Now run Model 2, which is similar to Model 1 except that the material constants are set to:

  .. math::

    c_{1} &= 0.0475~kPa\\
    c_{ff} &= 15.25 ~~~~
    c_{ss} &= 6.8 ~~~~
    c_{nn} &= 8.9 \\
    c_{fs} &= 6.95 ~~~~
    c_{fn} &= 6.05 ~~~~
    c_{ns} &= 4.93

  Re-use your analytical expressions from Step 1 above, now with these new material constants, to calculate **distortional components** of the second Piola-Kirchhoff stress tensor: :math:`T_{ref}^{ff\_dist}` and :math:`T_{ref}^{ss\_dist}` with respect to the reference axes.

|vspace|

8.  Re-use your analytical expressions from Step 4 above to calculate, for Model 2, the **total** stress components: :math:`T_{ref}^{ff}` and :math:`T_{ref}^{ss}` (use the new hydrostatic pressure value, :math:`p`, from the simulation results). Check your answers against the simulation results.

|vspace|

9. Explain the similarities and differences in the total second Piola-Kirchhoff stress components from Steps 5 and 8.  What can you infer about the mechanical responses (material symmetries) of the two models?

|vspace|

Stresses with respect to rotated material-fibre axes
----------------------------------------------------

10. Now run Model 5, which uses the same (anisotropic) material constants as in Step 7 above. In this simulation, the material-fibre axis is oriented at :math:`\theta=45` degrees with respect to the :math:`X_{1}`-axis (in the :math:`X_{1}`-:math:`X_{2}` plane). 

|vspace|

11. Substitute the fibre strain components (:math:`\boldsymbol{E}_{fib}`) from the simulation results, and the material constants from Step 7, into your expressions from Section 2 to determine the components of the total second Piola-Kirchhoff stress tensor with respect to the material-fibre coordinates, :math:`\boldsymbol{T}_{fib}` (use the hydrostatic pressure, :math:`p`, from the simulation results).

|vspace|

12. Determine the second Piola-Kirchhoff stress components with respect to the reference coordinate axes (:math:`\boldsymbol{T}_{ref}`) via an appropriate tensor transformation (see :ref:`Step 3 of Section 2 of Lab 2a <tensor_transformations>`). Check your answers against the simulation results.

|vspace|

13. How do the stress components of :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}` for this model compare to the components of :math:`\boldsymbol{T}_{ref}` for the previous model in Step 5 above? Explain the similarities and differences.

|vspace|

14. Now run Model 6, for which the material-fibre axis is oriented at :math:`\theta=90` degrees with respect to the :math:`X_{1}`-axis (in the :math:`X_{1}`-:math:`X_{2}` plane). Repeat the analyses in Steps 11-12.

|vspace|

15. How do the stress components of :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}` for this model compare to the components of :math:`\boldsymbol{T}_{ref}` for the previous model in Step 5 above? Explain the similarities and differences.

|vspace|


Extra discussion points for experts
-----------------------------------

If you have completed the exercises above, you may like to consider the following questions: 

a. What do you notice about the stress tensors, :math:`\boldsymbol{T}_{fib}` and :math:`\boldsymbol{T}_{ref}`, from the above analyses for the isotropic (Model 1) and anisotropic (Models 2,5,6) materials subject to equi-biaxial deformations? Explain this observation.

|vspace|

b. Model 1 considers equi-biaxial deformation, and there were similarities in some of the stress components. If, instead, a uniaxial stretch was applied along the :math:`X_{1}` direction, predict what would happed to the components of stress.

|vspace|

c. What would you expect if you compared the maximum principal stresses for each of the anisotropic cases (Models 2,5,6)? Justify your amswer.

|vspace|

.. note::

  By completing this lab, you should be able to:

    - derive expressions for the components of the second Piola-Kirchhoff stress tensor.

    - evaluate components of the second Piola-Kirchhoff stress tensor with respect to spatial or material-fibre coordinates.
    
    - infer the material symmetry of a material described by a specific constitutive equation and a particular set of material constants by analysing the stress components.

