# cara install module dari terminal = -d "nama_database" -u "nama_module"
from odoo import fields, models, api


class Users(models.Model):
    _inherit = 'res.users'

    nik = fields.Char(string='NIK', size=16)


class Masyarakat(models.Model):
    _name = 'pengmas.masyarakat'

    name = fields.Char('Nama', default=lambda self: self.env.user)
    nik = fields.Char('NIK', default=lambda self: self.env.nik)
    username = fields.Char('Username', default=lambda self: self.env.email)
    telp = fields.Char('Telp', default=lambda self: self.env.phone)
