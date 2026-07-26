.. _models:

Extra models
============

Model classes provide structured configuration for chart elements and features.

Annotations
-----------
.. currentmodule:: datawrapper.charts.annos

.. autoclass:: TextAnnotation
   :members:
   :show-inheritance:

.. autoclass:: RangeAnnotation
   :members:
   :show-inheritance:

.. autoclass:: XRangeAnnotation
   :members:
   :show-inheritance:

.. autoclass:: YRangeAnnotation
   :members:
   :show-inheritance:

.. autoclass:: XLineAnnotation
   :members:
   :show-inheritance:

.. autoclass:: YLineAnnotation
   :members:
   :show-inheritance:

.. autoclass:: AreaFill
   :members:
   :show-inheritance:

.. autoclass:: ConnectorLine
   :members:
   :show-inheritance:

Multiple Column Panels
----------------------
.. currentmodule:: datawrapper.charts.multiple_column

.. autoclass:: MultipleColumnPanel
   :members:
   :show-inheritance:

Column Format
-------------
.. currentmodule:: datawrapper.charts.models

.. autoclass:: ColumnFormat
   :members:
   :show-inheritance:

.. autoclass:: ColumnFormatList
   :members:
   :show-inheritance:

Data Changes
------------
.. currentmodule:: datawrapper.charts.models

``DataChange`` models individual cell corrections made in Datawrapper's
**Check & Describe** tab. Datawrapper stores these corrections under
``metadata.data.changes`` as zero-based row/column indexes, the replacement
``value``, an edit ``time`` in Unix milliseconds when available, and
``previous`` for overwritten cells. The ``previous`` field is optional because
Datawrapper omits it for entries such as added-column headers.

Datawrapper's developer docs show ``changes`` as a list. Existing API responses
can also return an object keyed by internal change IDs, with fields such as
``id``, ``ignored``, and ``_index``. ``Transform`` accepts both shapes and
round-trips object-shaped API responses without converting them to lists.

Live API smoke verification for this behavior used an authorized unpublished
Datawrapper test chart. The API accepted an object-map ``changes`` payload,
returned that object-map shape on read-back, and preserved the relevant
``id``, ``ignored``, and ``_index`` fields after a ``Transform``
deserialize/serialize write-back. The documented list-shaped compatibility
input was also accepted and read back as a list. The smoke restored the test
chart's corrections to an empty object and did not publish or verify behavior
for production-facing charts.

.. code-block:: python

   chart = dw.BarChart(
       title="Corrected values",
       data=df,
       transformations=dw.Transform(
           changes=[
               dw.DataChange(
                   row=9,
                   column=3,
                   value="1.7",
                   time=1573134075869,
                   previous="0.7",
               )
           ]
       ),
   )

.. autoclass:: DataChange
   :members:
   :show-inheritance:

.. autoclass:: DataChangeList
   :members:
   :show-inheritance:

Line Configuration
------------------
.. currentmodule:: datawrapper.charts.line

For practical workflow guidance, examples, and migration notes, see the
:doc:`LineChart guide </user-guide/charts/line-charts>`.

.. autoclass:: Line
   :members:
   :show-inheritance:

.. autoclass:: LineSymbol
   :members:
   :show-inheritance:

.. autoclass:: LineValueLabel
   :members:
   :show-inheritance:
