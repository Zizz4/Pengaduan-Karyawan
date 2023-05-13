from odoo import fields, models, api


class Petugas(models.Model):
    _name = 'pengmas.petugas'
    _order = 'id_petugas, name'

    id_petugas = fields.Integer('ID', size=11)
    name = fields.Char(string='Nama Petugas', size=35)
    username = fields.Char(string='Username', size=25)
    password = fields.Char(string='Password', size=32)
    telp = fields.Char(string='Telp', size=13)
    level = fields.Selection([
        ('admin', 'Admin'),
        ('petugas', 'Petugas')
    ])

