#!/usr/bin/env python
#> \file
#> \author Thiranja Babarenda Gamage
#> \brief 
#>
#> \section LICENSE
#>
#> Version: MPL 1.1/GPL 2.0/LGPL 2.1
#>
#> The contents of this file are subject to the Mozilla Public License
#> Version 1.1 (the "License"); you may not use this file except in
#> compliance with the License. You may obtain a copy of the License at
#> http://www.mozilla.org/MPL/
#>
#> Software distributed under the License is distributed on an "AS IS"
#> basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
#> License for the specific language governing rights and limitations
#> under the License.
#>
#> The Original Code is openCMISS
#>
#> The Initial Developer of the Original Code is University of Auckland,
#> Auckland, New Zealand and University of Oxford, Oxford, United
#> Kingdom. Portions created by the University of Auckland and University
#> of Oxford are Copyright (C) 2007 by the University of Auckland and
#> the University of Oxford. All Rights Reserved.
#>
#> Contributor(s): 
#>
#> Alternatively, the contents of this file may be used under the terms of
#> either the GNU General Public License Version 2 or later (the "GPL"), or
#> the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
#> in which case the provisions of the GPL or the LGPL are applicable instead
#> of those above. if you wish to allow use of your version of this file only
#> under the terms of either the GPL or the LGPL, and not to allow others to
#> use your version of this file under the terms of the MPL, indicate your
#> decision by deleting the provisions above and replace them with the notice
#> and other provisions required by the GPL or the LGPL. if you do not delete
#> the provisions above, a recipient may use your version of this file under
#> the terms of any one of the MPL, the GPL or the LGPL.
#>
#> Main script

import numpy
import math

# Intialise OpenCMISS
from opencmiss.iron import iron

# Set constants
X, Y, Z = (1, 2, 3)

# Set problem parameters
width = 1.0
length = 1.0
height = 1.0
UsePressureBasis = False
NumberOfGaussXi = 2

coordinateSystemUserNumber = 1
regionUserNumber = 1
basisUserNumber = 1
pressureBasisUserNumber = 2
generatedMeshUserNumber = 1
meshUserNumber = 1
decompositionUserNumber = 1

geometricFieldUserNumber = 1
fibreFieldUserNumber = 2
materialFieldUserNumber = 3
dependentFieldUserNumber = 4
equationsSetFieldUserNumber = 5
deformedFieldUserNumber = 7
pressureFieldUserNumber = 8

equationsSetUserNumber = 1
problemUserNumber = 1

# Set all diganostic levels on for testing
#iron.DiagnosticsSetOn(iron.DiagnosticTypes.ALL,[1,2,3,4,5],"diagnostics.txt",[])

numberOfLoadIncrements = 1
numberGlobalXElements = 1
numberGlobalYElements = 1
numberGlobalZElements = 1
InterpolationType = 1
numberOfXi = 3

def solve_model(exportname, model=1, debug=False):
    # Setting debug=False will prevent output of solver progress/results to the screen.
    if debug:
        print("Solving model {0}".format(model))

    # Get the number of computational nodes and this computational node number
    numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
    # computationalNodeNumber = iron.ComputationalNodeNumberGet()

    # Create a 3D rectangular cartesian coordinate system
    coordinateSystem = iron.CoordinateSystem()
    coordinateSystem.CreateStart(coordinateSystemUserNumber)
    coordinateSystem.DimensionSet(3)
    coordinateSystem.CreateFinish()

    # Create a region and assign the coordinate system to the region
    region = iron.Region()
    region.CreateStart(regionUserNumber,iron.WorldRegion)
    region.LabelSet("Region")
    region.coordinateSystem = coordinateSystem
    region.CreateFinish()

    # Define basis
    basis = iron.Basis()
    basis.CreateStart(basisUserNumber)
    if InterpolationType in (1,2,3,4):
        basis.type = iron.BasisTypes.LAGRANGE_HERMITE_TP
    elif InterpolationType in (7,8,9):
        basis.type = iron.BasisTypes.SIMPLEX
    basis.numberOfXi = numberOfXi
    basis.interpolationXi = (
        [iron.BasisInterpolationSpecifications.LINEAR_LAGRANGE]*numberOfXi)
    if(NumberOfGaussXi>0):
        basis.quadratureNumberOfGaussXi = [NumberOfGaussXi]*numberOfXi
    basis.CreateFinish()

    if(UsePressureBasis):
        # Define pressure basis
        pressureBasis = iron.Basis()
        pressureBasis.CreateStart(pressureBasisUserNumber)
        if InterpolationType in (1,2,3,4):
            pressureBasis.type = iron.BasisTypes.LAGRANGE_HERMITE_TP
        elif InterpolationType in (7,8,9):
            pressureBasis.type = iron.BasisTypes.SIMPLEX
        pressureBasis.numberOfXi = numberOfXi
        pressureBasis.interpolationXi = (
            [iron.BasisInterpolationSpecifications.LINEAR_LAGRANGE]*numberOfXi)
        if(NumberOfGaussXi>0):
            pressureBasis.quadratureNumberOfGaussXi = [NumberOfGaussXi]*numberOfXi
        pressureBasis.CreateFinish()

    # Start the creation of a generated mesh in the region
    generatedMesh = iron.GeneratedMesh()
    generatedMesh.CreateStart(generatedMeshUserNumber,region)
    generatedMesh.type = iron.GeneratedMeshTypes.REGULAR
    if(UsePressureBasis):
        generatedMesh.basis = [basis,pressureBasis]
    else:
        generatedMesh.basis = [basis]
        generatedMesh.extent = [width,length,height]
        generatedMesh.numberOfElements = (
            [numberGlobalXElements,numberGlobalYElements,numberGlobalZElements])
    # Finish the creation of a generated mesh in the region
    mesh = iron.Mesh()
    generatedMesh.CreateFinish(meshUserNumber,mesh)

    # Create a decomposition for the mesh
    decomposition = iron.Decomposition()
    decomposition.CreateStart(decompositionUserNumber,mesh)
    decomposition.type = iron.DecompositionTypes.CALCULATED
    decomposition.numberOfDomains = numberOfComputationalNodes
    decomposition.CreateFinish()

    # Create a field for the geometry
    geometricField = iron.Field()
    geometricField.CreateStart(geometricFieldUserNumber,region)
    geometricField.MeshDecompositionSet(decomposition)
    geometricField.TypeSet(iron.FieldTypes.GEOMETRIC)
    geometricField.VariableLabelSet(iron.FieldVariableTypes.U,"Geometry")
    geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,1,1)
    geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,2,1)
    geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,3,1)
    if InterpolationType == 4:
        geometricField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
    geometricField.CreateFinish()

    # Update the geometric field parameters from generated mesh
    generatedMesh.GeometricParametersCalculate(geometricField)

    # Create a fibre field and attach it to the geometric field
    fibreField = iron.Field()
    fibreField.CreateStart(fibreFieldUserNumber,region)
    fibreField.TypeSet(iron.FieldTypes.FIBRE)
    fibreField.MeshDecompositionSet(decomposition)
    fibreField.GeometricFieldSet(geometricField)
    fibreField.VariableLabelSet(iron.FieldVariableTypes.U,"Fibre")
    if InterpolationType == 4:
        fibreField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
    fibreField.CreateFinish()

    # Create a deformed geometry field, as Cmgui/Zinc doesn't like displaying
    # deformed fibres from the dependent field because it isn't a geometric field.
    deformedField = iron.Field()
    deformedField.CreateStart(deformedFieldUserNumber, region)
    deformedField.MeshDecompositionSet(decomposition)
    deformedField.TypeSet(iron.FieldTypes.GEOMETRIC)
    deformedField.VariableLabelSet(iron.FieldVariableTypes.U, "DeformedGeometry")
    for component in [1, 2, 3]:
        deformedField.ComponentMeshComponentSet(
                iron.FieldVariableTypes.U, component, 1)
    if InterpolationType == 4:
        deformedField.ScalingTypeSet(iron.FieldScalingTypes.ARITHMETIC_MEAN)
    deformedField.CreateFinish()

    pressureField = iron.Field()
    pressureField.CreateStart(pressureFieldUserNumber, region)
    pressureField.MeshDecompositionSet(decomposition)
    pressureField.VariableLabelSet(iron.FieldVariableTypes.U, "Pressure")
    pressureField.ComponentMeshComponentSet(
            iron.FieldVariableTypes.U, 1, 1)
    pressureField.ComponentInterpolationSet(iron.FieldVariableTypes.U, 1, iron.FieldInterpolationTypes.ELEMENT_BASED)
    pressureField.NumberOfComponentsSet(iron.FieldVariableTypes.U, 1)
    pressureField.CreateFinish()

    # Create the equations_set
    equationsSetField = iron.Field()
    equationsSet = iron.EquationsSet()

    problemSpecification = [iron.ProblemClasses.ELASTICITY,
        iron.ProblemTypes.FINITE_ELASTICITY,
        iron.EquationsSetSubtypes.ORTHOTROPIC_MATERIAL_COSTA]
    equationsSet.CreateStart(equationsSetUserNumber,region,fibreField,problemSpecification,
        equationsSetFieldUserNumber, equationsSetField)
    equationsSet.CreateFinish()

    # Create the dependent field
    dependentField = iron.Field()
    equationsSet.DependentCreateStart(dependentFieldUserNumber,dependentField)
    dependentField.VariableLabelSet(iron.FieldVariableTypes.U,"Dependent")
    dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.U,4,iron.FieldInterpolationTypes.ELEMENT_BASED)
    dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.DELUDELN,4,iron.FieldInterpolationTypes.ELEMENT_BASED)
    if(UsePressureBasis):
        # Set the pressure to be nodally based and use the second mesh component
        if InterpolationType == 4:
            dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.U,4,iron.FieldInterpolationTypes.NODE_BASED)
            dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.DELUDELN,4,iron.FieldInterpolationTypes.NODE_BASED)
        dependentField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,4,2)
        dependentField.ComponentMeshComponentSet(iron.FieldVariableTypes.DELUDELN,4,2)
    if InterpolationType == 4:
        dependentField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
    equationsSet.DependentCreateFinish()

    # Create the material field
    materialField = iron.Field()
    equationsSet.MaterialsCreateStart(materialFieldUserNumber,materialField)
    materialField.VariableLabelSet(iron.FieldVariableTypes.U,"Material")
    equationsSet.MaterialsCreateFinish()

    # Set Costa constitutive relation parameters.
    # Q=[c_ff 2c_fs 2c_fn c_ss 2c_ns c_nn]' * [E_ff E_fs  E_fn  E_ss E_sn  E_nn].^2;
    if model in [1, 3, 4]:
        c_1 = 0.0475
        c_ff = 15.25
        c_fs = 6.05
        c_fn = c_fs
        c_ss = c_ff
        c_sn = c_fs
        c_nn = c_ff
    elif model in [2, 5, 6]:
        c_1 = 0.0475
        c_ff = 15.25
        c_fs = 6.95
        c_fn = 6.05
        c_ss = 6.8
        c_sn = 4.93
        c_nn = 8.9

    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,c_1)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,2,c_ff)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,3,c_fs)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,4,c_fn)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,5,c_ss)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,6,c_sn)
    materialField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,7,c_nn)

    if model in [1, 2]:
        angle = numpy.deg2rad(0.)
    elif model == 3:
        angle = numpy.deg2rad(30.)
    elif model in [4, 5]:
        angle = numpy.deg2rad(45.)
    elif model ==6:
        angle = numpy.deg2rad(90.)

    fibreField.ComponentValuesInitialiseDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,angle)


    # Create equations
    equations = iron.Equations()
    equationsSet.EquationsCreateStart(equations)
    equations.sparsityType = iron.EquationsSparsityTypes.SPARSE
    equations.outputType = iron.EquationsOutputTypes.NONE
    equationsSet.EquationsCreateFinish()

    # Initialise dependent field from undeformed geometry and displacement bcs and set hydrostatic pressure
    iron.Field.ParametersToFieldParametersComponentCopy(
        geometricField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,
        dependentField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1)
    iron.Field.ParametersToFieldParametersComponentCopy(
        geometricField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,2,
        dependentField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,2)
    iron.Field.ParametersToFieldParametersComponentCopy(
        geometricField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,3,
        dependentField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,3)
    iron.Field.ComponentValuesInitialiseDP(
        dependentField,iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,4,0.0)

    # Define the problem
    problem = iron.Problem()
    problemSpecification = [iron.ProblemClasses.ELASTICITY,
            iron.ProblemTypes.FINITE_ELASTICITY,
            iron.ProblemSubtypes.NONE]
    problem.CreateStart(problemUserNumber, problemSpecification)
    problem.CreateFinish()

    # Create the problem control loop
    problem.ControlLoopCreateStart()
    controlLoop = iron.ControlLoop()
    problem.ControlLoopGet([iron.ControlLoopIdentifiers.NODE],controlLoop)
    controlLoop.MaximumIterationsSet(numberOfLoadIncrements)
    problem.ControlLoopCreateFinish()

    # Create problem solver
    nonLinearSolver = iron.Solver()
    linearSolver = iron.Solver()
    problem.SolversCreateStart()
    problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,nonLinearSolver)
    if debug:
        nonLinearSolver.outputType = iron.SolverOutputTypes.PROGRESS
    else:
        nonLinearSolver.outputType = iron.SolverOutputTypes.NONE
    nonLinearSolver.NewtonJacobianCalculationTypeSet(
            iron.JacobianCalculationTypes.EQUATIONS)
    nonLinearSolver.NewtonLinearSolverGet(linearSolver)
    linearSolver.linearType = iron.LinearSolverTypes.DIRECT
    #linearSolver.libraryType = iron.SolverLibraries.LAPACK
    problem.SolversCreateFinish()

    # Create solver equations and add equations set to solver equations
    solver = iron.Solver()
    solverEquations = iron.SolverEquations()
    problem.SolverEquationsCreateStart()
    problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
    solver.SolverEquationsGet(solverEquations)
    solverEquations.sparsityType = iron.SolverEquationsSparsityTypes.SPARSE
    _ = solverEquations.EquationsSetAdd(equationsSet)
    problem.SolverEquationsCreateFinish()

    # Prescribe boundary conditions (absolute nodal parameters)
    boundaryConditions = iron.BoundaryConditions()
    solverEquations.BoundaryConditionsCreateStart(boundaryConditions)

    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,1,X,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,3,X,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,5,X,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,7,X,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,2,X,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,4,X,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,6,X,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,8,X,iron.BoundaryConditionsTypes.FIXED,0.25)

    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,1,Y,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,2,Y,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,5,Y,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,6,Y,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,3,Y,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,4,Y,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,7,Y,iron.BoundaryConditionsTypes.FIXED,0.25)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,8,Y,iron.BoundaryConditionsTypes.FIXED,0.25)


    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,1,Z,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,2,Z,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,3,Z,iron.BoundaryConditionsTypes.FIXED,0.0)
    boundaryConditions.AddNode(dependentField,iron.FieldVariableTypes.U,1,1,4,Z,iron.BoundaryConditionsTypes.FIXED,0.0)

    solverEquations.BoundaryConditionsCreateFinish()

    # Solve the problem
    problem.Solve()

    # Copy deformed geometry into deformed field
    for component in [1, 2, 3]:
        dependentField.ParametersToFieldParametersComponentCopy(
            iron.FieldVariableTypes.U,
            iron.FieldParameterSetTypes.VALUES, component,
            deformedField, iron.FieldVariableTypes.U,
            iron.FieldParameterSetTypes.VALUES, component)

    # Copy pressure into pressure field
    dependentField.ParametersToFieldParametersComponentCopy(
            iron.FieldVariableTypes.U,
            iron.FieldParameterSetTypes.VALUES, 4,
            pressureField, iron.FieldVariableTypes.U,
            iron.FieldParameterSetTypes.VALUES, 1)

    # Export results
    fields = iron.Fields()
    fields.CreateRegion(region)
    fields.NodesExport(exportname,"FORTRAN")
    fields.ElementsExport(exportname,"FORTRAN")
    fields.Finalise()

    Q = numpy.array([[numpy.cos(angle), -numpy.sin(angle),  0.],
                     [numpy.sin(angle), numpy.cos(angle) ,  0.],
                     [0.              , 0.               ,  1.]])

    results = {}
    elementNumber = 1
    xiPosition = [0.5, 0.5, 0.5]
    # Note that there seems to be a bug with F in OpenCMISS when fibre angles are specified in x1-x2 plane
    #F = equationsSet.TensorInterpolateXi(
    #    iron.EquationsSetTensorEvaluateTypes.DEFORMATION_GRADIENT,
    #    elementNumber, xiPosition,(3,3))
    Ffib = numpy.array([[0.1250E+01, 0.        , 0.],
                        [0.        , 0.1250E+01, 0.],
                        [0.        , 0.        , 0.6400E+00]])
    Fref = Ffib
    results["Deformation gradient tensor (fibre coordinate system)"] = Ffib
    results["Deformation gradient tensor (reference coordinate system)"] = Fref
    if debug:
        print("Deformation gradient tensor (fibre coordinate system)")
        print(Ffib)
        print("Deformation gradient tensor (reference coordinate system)")
        print(Fref)

    Cfib = equationsSet.TensorInterpolateXi(
        iron.EquationsSetTensorEvaluateTypes.R_CAUCHY_GREEN_DEFORMATION,
        elementNumber, xiPosition,(3,3))
    Cref=Cfib
    results["Right Cauchy-Green deformation tensor (fibre coordinate system)"] = Cfib
    results["Right Cauchy-Green deformation tensor (reference coordinate system)"] = Cref
    if debug:
        print("Right Cauchy-Green deformation tensor (fibre coordinate system)")
        print(Cfib)
        print("Right Cauchy-Green deformation tensor (reference coordinate system)")
        print(Cref)

    Efib = equationsSet.TensorInterpolateXi(
        iron.EquationsSetTensorEvaluateTypes.GREEN_LAGRANGE_STRAIN,
        elementNumber, xiPosition,(3,3))
    results["Green-Lagrange strain tensor (fibre coordinate system)"] = Efib
    if debug:
        print("Green-Lagrange strain tensor (fibre coordinate system)")
        print(Efib)

    Eref = numpy.dot(Q,numpy.dot(Efib,numpy.matrix.transpose(Q)))
    results["Green-Lagrange strain tensor (reference coordinate system)"] = Eref
    if debug:
        print("Green-Lagrange strain tensor (reference coordinate system)")
        print(Eref)

    I1=numpy.trace(Cfib)
    I2=0.5*(numpy.trace(Cfib)**2.-numpy.tensordot(Cfib,Cfib))
    I3=numpy.linalg.det(Cfib)
    results["Invariants of Cfib (fibre coordinate system)"] = [I1, I2, I3]
    if debug:
        print("Invariants of Cfib (fibre coordinate system)")
        print("I1={0}, I2={1}, I3={2}".format(I1,I2,I3))

    I1=numpy.trace(Cref)
    I2=0.5*(numpy.trace(Cref)**2.-numpy.tensordot(Cref,Cref))
    I3=numpy.linalg.det(Cref)
    results["Invariants of Cref (reference coordinate system)"] = [I1, I2, I3]
    if debug:
        print("Invariants of Cref (reference coordinate system)")
        print("I1={0}, I2={1}, I3={2}".format(I1,I2,I3))

    TCref = equationsSet.TensorInterpolateXi(
        iron.EquationsSetTensorEvaluateTypes.CAUCHY_STRESS,
        elementNumber, xiPosition,(3,3))
    results["Cauchy stress tensor (reference coordinate system)"] = TCref
    if debug:
        print("Cauchy stress tensor (reference coordinate system)")
        print(TCref)

    # Output of Second Piola-Kirchhoff Stress Tensor not implemented. It is
    # instead, calculated from TG=J*F^(-1)*TC*F^(-T), where T indicates the
    # transpose fo the matrix.
    #TG = equationsSet.TensorInterpolateXi(
    #    iron.EquationsSetTensorEvaluateTypes.SECOND_PK_STRESS,
    #    elementNumber, xiPosition,(3,3))
    #J=1. #Assumes J=1
    TGref = numpy.dot(numpy.linalg.inv(Fref),numpy.dot(
            TCref,numpy.linalg.inv(numpy.matrix.transpose(Fref))))
    results["Second Piola-Kirchhoff stress tensor (reference coordinate system)"] = TGref
    if debug:
        print("Second Piola-Kirchhoff stress tensor (reference coordinate system)")
        print(TGref)

    TGfib = numpy.dot(numpy.matrix.transpose(Q),numpy.dot(TGref,Q))
    results["Second Piola-Kirchhoff stress tensor (fibre coordinate system)"] = TGfib
    if debug:
        print("Second Piola-Kirchhoff stress tensor (fibre coordinate system)")
        print(TGfib)

    # Note that the hydrostatic pressure value is different from the value quoted
    # in the original lab instructions. This is because the stress has been
    # evaluated using modified invariants (isochoric invariants)
    p = -dependentField.ParameterSetGetElement(
        iron.FieldVariableTypes.U,
        iron.FieldParameterSetTypes.VALUES,elementNumber,4)
    results["Hydrostatic pressure"] = p
    if debug:
        print("Hydrostatic pressure")
        print(p)

    problem.Destroy()
    coordinateSystem.Destroy()
    region.Destroy()
    basis.Destroy()

    return results


if __name__ == "__main__":
    exportname = "model1"
    results = solve_model(exportname, model=1, debug=True)
    exportname = "model2"
    results = solve_model(exportname, model=2, debug=True)
    exportname = "model3"
    results = solve_model(exportname, model=3, debug=True)
    exportname = "model4"
    results = solve_model(exportname, model=4, debug=True)
    exportname = "model5"
    results = solve_model(exportname, model=5, debug=True)
    exportname = "model6"
    results = solve_model(exportname, model=6, debug=True)


