from odoo import fields, models, api


class TotalPengaduan(models.Model):
    _name = 'pengmas.total.pengaduan'

    pengaduan_ids = fields.One2many('pengmas.pengaduan', 'id_pengaduan', string='Pengaduan')
    bulan = fields.Char('Bulan', compute='_ambil_data_bulan')

    @api.depends('pengaduan_ids')
    def _ambil_data_bulan(self):
        for rec in self:
            data = rec.pengaduan_ids.bulan
            if data:
                rec.bulan = data
            else:
                rec.bulan = "FALSE"
