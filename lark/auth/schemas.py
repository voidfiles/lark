import colander


class ClientSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    default_scope = colander.SchemaNode(colander.String(), missing='')
    redirect_uris = colander.SchemaNode(colander.Sequence(colander.String),
                                        missing=['http://localhost:8000'])
