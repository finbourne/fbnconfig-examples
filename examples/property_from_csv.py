import csv
import os

from fbnconfig import Deployment, datatype, property


def configure(env):
    deployment_name = getattr(env, "name", "propertiesFromCsv")
    properties = []
    # Reuse a single DataTypeRef per (scope, code) across the loop so the
    # dump emits `{$ref: ...}` and matches the schema, and so we don't
    # explode the dependency graph with duplicates.
    data_type_refs: dict[tuple[str, str], datatype.DataTypeRef] = {}

    csv_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "data", "property_definitions.csv"
    )

    # Read the CSV file
    with open(csv_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        # Parse each row and create Property instances
        for row in reader:
            domain = row["Domain"]
            scope = row["PropertyScope"]
            code = row["PropertyCode"]
            dt_scope = row["DataTypeScope"]
            dt_code = row["DataTypeCode"]
            dt_key = (dt_scope, dt_code)
            if dt_key not in data_type_refs:
                data_type_refs[dt_key] = datatype.DataTypeRef(
                    id=f"datatype-{dt_scope}-{dt_code}",
                    scope=dt_scope,
                    code=dt_code,
                )
            property_definition = property.DefinitionResource(
                id=f"property-{domain}-{scope}-{code}",
                domain=property.Domain[domain],
                scope=scope,
                code=code,
                display_name=row["DisplayName"],
                data_type_id=data_type_refs[dt_key],
                constraint_style=property.ConstraintStyle[row["ConstraintStyle"]],
                property_description=row["Description"],
                life_time=property.LifeTime[row["Lifetime"]],
                collection_type=None,
            )
            properties.append(property_definition)

    return Deployment(deployment_name, properties)
