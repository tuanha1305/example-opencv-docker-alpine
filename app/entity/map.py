from marshmallow import Schema, fields


class MarkerSchema(Schema):
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    url = fields.URL(required=True)


class DataSchema(Schema):
    map = fields.Dict(required=True)
    marker = fields.Nested(MarkerSchema, required=True)
    places = fields.String()


class MapInfoSchema(Schema):
    style = fields.String(required=True)
    zoom = fields.String(required=True)
    align = fields.String(required=True)


class MapSchema(Schema):
    mapInfo = fields.Nested(MapInfoSchema, required=True)
    data = fields.Nested(DataSchema, required=True)
    resultfile = fields.String(required=True)
