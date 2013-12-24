import collander


def ClientSchema(collander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    description = colander.SchemaNode(colander.String())
    default_scope = colander.SchemaNode(colander.Strin(), missing='')
    redirect_uris = colander.SchemaNode(colander.Sequence(colander.String),
                                        missing=['http://localhost:8000'])
