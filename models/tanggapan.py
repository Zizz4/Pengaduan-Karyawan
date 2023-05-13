from odoo import fields, models, api
from datetime import datetime

class Tanggapan(models.Model):
    _name = 'pengmas.tanggapan'

    def _compute_pengaduan_name(self):
        for attachment in self:
            if attachment.res_model and attachment.res_id:
                record = self.env[attachment.res_model].browse(attachment.res_id)
                attachment.id_pengaduan = record.id
            else:
                attachment.id_pengaduan = False

    id_tanggapan = fields.Integer(string='ID', size=11)
    name = fields.Char("Judul", required=True)
    id_pengaduan = fields.Many2one('pengmas.pengaduan', compute='_compute_pengaduan_name')
    tgl_tanggapan = fields.Date(string='Tanggal', default=lambda self: datetime.today().date())
    id_petugas = fields.Char(string='Petugas', required=True, default=lambda self: self.env.user.name)
    tanggapan = fields.Text(string='Tanggapan', required=True)

    res_model = fields.Char('Resource Model', readonly=True, help="The database object this attachment will be attached to.")
    res_id = fields.Many2oneReference('Resource ID', model_field='res_model',
                                      readonly=True, help="The record id this is attached to.")

