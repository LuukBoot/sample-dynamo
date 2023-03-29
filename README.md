# Tuturial dynamo 

## Introduction 

In this tutorial, we will learn how to seamlessly integrate a dynamo model into the Viktor platform. With the help of Dynamo Sandbox, a visual programming tool for creating complex parametric models, we can efficiently produce accurate 3D models. In this tutorial, we will render a house, and assume that the dynamo file has already been created.

To start, the user provides the necessary parameters for the dynamo model within the Viktor application. The Viktor worker then computes the dynamo model using the command-line interface included within Dynamo Sandbox. The geometry of the model is generated using either Autodesk Revit or FormIt. The geometry JSON is then converted to a mesh, which is rendered and visualized in Viktor.

In addition to creating the app, this tutorial will also cover common troubleshooting issues that may arise during the integration process. Furthermore, we will discuss how to install the worker, which is required to run the analysis.