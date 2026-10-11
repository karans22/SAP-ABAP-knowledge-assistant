# CDS Views in ABAP

Core Data Services (CDS) views are used to define semantically rich data
models directly in the database layer, pushing calculations and
aggregations down to the database instead of the ABAP application layer.

## Key concepts

- **Basic Interface View**: Exposes raw table data with minimal logic,
  typically prefixed `I_` (e.g. `I_SalesOrder`).
- **Composite/Consumption View**: Built on top of basic views, adds
  associations, joins, and business logic. Often exposed via OData for
  Fiori apps.
- **Annotations**: Metadata such as `@UI`, `@Search`, `@Analytics` control
  how the view is rendered in Fiori Elements apps or used in analytics.
- **Associations**: Declared relationships between CDS views (similar to
  foreign keys) that can be resolved on demand instead of always joining,
  improving performance.

## Common patterns

```abap
@AbapCatalog.sqlViewName: 'ZSDORDERITEMS'
@AccessControl.authorizationCheck: #CHECK
define view ZI_SalesOrderItems
  as select from vbap as item
  association [1..1] to vbak as _Header on $projection.SalesOrder = _Header.Vbeln
{
  key item.vbeln as SalesOrder,
  key item.posnr as ItemNumber,
      item.matnr as Material,
      _Header
}
```

## Common errors

- **CDS view activation fails with "Element does not exist"**: usually
  caused by a typo in the source field name or a missing association
  alias reference.
- **Association not resolving in Fiori app**: check that the association
  is marked `redirected to` the correct consumption view if the
  association target has multiple implementations.
- **Performance issues with CDS views**: often caused by unnecessary
  joins instead of associations, or missing `@ObjectModel.usageType`
  annotations that prevent the optimizer from pushing filters down.
