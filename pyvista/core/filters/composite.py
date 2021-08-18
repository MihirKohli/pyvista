"""Filters module with a class to manage filters/algorithms for composite datasets."""
import pyvista
from pyvista import abstract_class, _vtk, wrap
from pyvista.core.filters.data_set import DataSetFilters


@abstract_class
class CompositeFilters:
    """An internal class to manage filters/algorithms for composite datasets."""

    def extract_geometry(composite):
        """Combine the geometry of all blocks into a single ``PolyData`` object.

        Place this filter at the end of a pipeline before a polydata
        consumer such as a polydata mapper to extract geometry from all blocks
        and append them to one polydata object.

        """
        gf = _vtk.vtkCompositeDataGeometryFilter()
        gf.SetInputData(composite)
        gf.Update()
        return wrap(gf.GetOutputDataObject(0))

    def combine(composite, merge_points=False, tolerance=0.0):
        """Combine all blocks into a single unstructured grid.

        Parameters
        ----------
        merge_points : bool, optional
            Merge coincidental points.

        tolerance : float
            The tolerance to use to find coincident points when
            ``merge_points=True``.

        Examples
        --------
        Combine blocks within a multiblock without merging points.

        >>> import pyvista
        >>> block = pyvista.MultiBlock([pyvista.Cube(),
        ...                             pyvista.Cube(center=(1, 0, 0))])
        >>> merged = block.combine()
        >>> merged.n_points
        48

        Combine blocks and merge points

        >>> merged = block.combine(merge_points=True)
        >>> merged.n_points
        12

        """
        alg = _vtk.vtkAppendFilter()
        for block in composite:
            if isinstance(block, _vtk.vtkMultiBlockDataSet):
                block = CompositeFilters.combine(block, merge_points=merge_points)
            alg.AddInputData(block)
        alg.SetMergePoints(merge_points)
        alg.Update()
        return wrap(alg.GetOutputDataObject(0))

    clip = DataSetFilters.clip

    clip_box = DataSetFilters.clip_box

    slice = DataSetFilters.slice

    slice_orthogonal = DataSetFilters.slice_orthogonal

    slice_along_axis = DataSetFilters.slice_along_axis

    slice_along_line = DataSetFilters.slice_along_line

    extract_all_edges = DataSetFilters.extract_all_edges

    elevation = DataSetFilters.elevation

    compute_cell_sizes = DataSetFilters.compute_cell_sizes

    cell_centers = DataSetFilters.cell_centers

    cell_data_to_point_data = DataSetFilters.cell_data_to_point_data

    point_data_to_cell_data = DataSetFilters.point_data_to_cell_data

    triangulate = DataSetFilters.triangulate

    def outline(composite, generate_faces=False, nested=False, progress_bar=False):
        """Produce an outline of the full extent for the all blocks in this composite dataset.

        Parameters
        ----------
        generate_faces : bool, optional
            Generate solid faces for the box. This is off by default

        nested : bool, optional
            If True, these creates individual outlines for each nested dataset

        progress_bar : bool, optional
            Display a progress bar to indicate progress.

        """
        if nested:
            return DataSetFilters.outline(composite, generate_faces=generate_faces, progress_bar=progress_bar)
        box = pyvista.Box(bounds=composite.bounds)
        return box.outline(generate_faces=generate_faces, progress_bar=progress_bar)

    def outline_corners(composite, factor=0.2, nested=False, progress_bar=False):
        """Produce an outline of the corners for the all blocks in this composite dataset.

        Parameters
        ----------
        factor : float, optional
            controls the relative size of the corners to the length of the
            corresponding bounds

        nested : bool, optional
            If True, these creates individual outlines for each nested dataset

        progress_bar : bool, optional
            Display a progress bar to indicate progress.

        """
        if nested:
            return DataSetFilters.outline_corners(composite, factor=factor, progress_bar=progress_bar)
        box = pyvista.Box(bounds=composite.bounds)
        return box.outline_corners(factor=factor, progress_bar=progress_bar)
