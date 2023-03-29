from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, NumberField
from viktor.views import GeometryAndDataView, GeometryAndDataResult, GeometryView, GeometryResult
from viktor.external.generic import GenericAnalysis
from viktor.external.dynamo import DynamoFile, convert_geometry_to_glb
from viktor.core import File
from pathlib import Path

class Parametrization(ViktorParametrization):

    # Input fields
    number_of_houses = NumberField("Number of houses", max=8.0, min=1.0, variant='slider', step=1.0, default=3.0)
    number_of_floors = NumberField("Number of floors", max=5.0, min=1.0, variant='slider', step=1.0, default=2.0)
    depth = NumberField("Depth [m]", max=10.0, min=5.0, variant='slider', step=1.0, default=8.0)
    width = NumberField("Width [m]", max=6.0, min=4.0, variant='slider', step=1.0, default=5.0)
    height_floor = NumberField("Height floor", max=3.0, min=2.0, variant='slider', step=0.1, default=2.5, suffix='m')
    height_roof = NumberField("Height roof", max=3.0, min=2.0, variant='slider', step=0.1, default=2.5, suffix='m')
    


class Controller(ViktorController):
    viktor_enforce_field_constraints = True  # Resolves upgrade instruction https://docs.viktor.ai/sdk/upgrades#U83

    label = 'My Entity Type'
    parametrization = Parametrization

    @staticmethod
    def update_model(params):
        """This method updates the nodes of the dynamo file with the parameters 
        from the parametrization class."""

        # First the path to the dynamo file is specified and loaded
        file_path = Path(__file__).parent / "dynamo_model_sample_app.dyn"
        _file = File.from_path(file_path)
        dyn_file  = DynamoFile(_file)

        # Update dynamo file with parameters from user input
        dyn_file.update("Number of houses", params.number_of_houses)
        dyn_file.update("Number of floors", params.number_of_floors)
        dyn_file.update("Depth", params.depth)
        dyn_file.update("Width", params.width)
        dyn_file.update("Height floor", params.height_floor)
        dyn_file.update("Height roof", params.height_roof)

        # generate updated file
        input_file = dyn_file.generate()

        return input_file


    @GeometryView("Building 3D", duration_guess=5)
    def geometry_and_data_view(self, params, **kwargs):

        # Step 1: Update model 
        input_file = self.update_model(params)

        # Step 2: Running analyses 
        files = [
        ('input.dyn', input_file),
        ]

        generic_analysis = GenericAnalysis(files=files, executable_key="dynamo", output_filenames=["output.xml", "geometry.json"])
        generic_analysis.execute(timeout=60)

        # Step 3: Processing geometry
        geometry_file = generic_analysis.get_output_file('geometry.json', as_file=True)
        glb_file = convert_geometry_to_glb(geometry_file)

        return GeometryResult(glb_file)