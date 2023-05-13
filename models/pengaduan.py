from odoo import fields, models, api
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Pengaduan(models.Model):
    _name = 'pengmas.pengaduan'
    _order = 'name'

    id_pengaduan = fields.Many2one('pengmas.total.pengaduan', string="Pengaduan")
    name = fields.Char(string="Judul", required=True)
    user_id = fields.Many2one(
        'res.users', string='Penulis', index=True, default=lambda self: self.env.user)
    tanggal = fields.Date(string='Tanggal', default=lambda self: datetime.today().date())
    nik = fields.Char(string='NIK', size=16, required=True, default=lambda self: self.env.user.nik)
    isi_laporan = fields.Text(string='Isi Laporan', required=True)
    foto = fields.Image(string='Foto', max_width=1024, max_height=1024)
    state = fields.Selection([
        ('0', 'Draft'),
        ('proses', 'Proses'),
        ('selesai', 'Selesai')
    ], string='Status', readonly=True, required=True, tracking=True, copy=False, default='0')
    group_pengmas_masyarakat = fields.Boolean("Masyarakat", implied_group="pengmas.group_pengmas_masyarakat")
    group_pengmas_petugas = fields.Boolean("Petugas", implied_group='pengmas.group_pengmas_petugas')
    group_pengmas_admin = fields.Boolean("Admin", implied_group="pengmas.group_pengmas_admin")

    #
    # total_pengaduan = fields.Integer(string='Total Pengaduan', compute='_hitung_pengaduan')
    # bulan = fields.Char(string='Bulan', compute='_ambil_bulan')
    #
    # jumlah_data_proses = fields.Integer(string='Jumlah Data', compute='_jumlah_data_proses')
    # jumlah_data_selesai = fields.Integer(string='Jumlah Data', compute='_jumlah_data_selesai')

    # @api.depends('tgl_pengaduan')
    # def _ambil_bulan(self):
    #     for record in self:
    #         data = record.tgl_pengaduan
    #         if data:
    #             record.bulan = datetime.strptime(str(record.tgl_pengaduan), "%Y-%m-%d").strftime('%B')
    #         else:
    #             record.bulan = "ANJAS KELAS"
    #
    # def _jumlah_data_proses(self):
    #     for rec in self:
    #         rec.jumlah_data_proses = self.env['pengmas.pengaduan'].search_count([('state', '=', 'proses')])
    #
    # def _jumlah_data_selesai(self):
    #     for rec in self:
    #         rec.jumlah_data_selesai = self.env['pengmas.pengaduan'].search_count([('state', '=', 'selesai')])

    # def _hitung_pengaduan(self):
    #     for record in self:
    #         data = record.ids
    #         jumlah_data = len(data)
    #         if data and jumlah_data:
    #             record.total_pengaduan = jumlah_data

    def tanggapan_action(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('pengmas.action_tanggapan')
        res['domain'] = [('res_model', '=', 'pengmas.pengaduan'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'pengmas.pengaduan', 'default_res_id': self.id}
        return res

    def kirim_pengaduan(self):
        self.write({'state': 'proses'})
        target_model = self.env['jumlah.data']
        target_model.create({'pengaduan_id': self.name, 'tanggal': self.tanggal, 'state': self.state})

    def validasi_pengaduan(self):
        self.write({'state': 'selesai'})
        target_model = self.env['jumlah.data']
        target_model.write({'state': self.state})


class JumlahData(models.Model):
    _name = 'jumlah.data'

    pengaduan_id = fields.Char(string='Penulis')
    tanggal = fields.Date(string="Tanggal")
    state = fields.Char(string="Status")
    bulan = fields.Char(string="Bulan", compute='_ambil_bulan')
    jumlah_proses_per_bulan = fields.Integer(string='Jumlah Proses', compute='_jumlah_proses')
    jumlah_selesai_per_bulan = fields.Integer(string='Jumlah Selesai', compute='_jumlah_selesai')

    @api.depends('tanggal')
    def _ambil_bulan(self):
        for record in self:
            data = record.tanggal
            if data:
                record.bulan = datetime.strptime(str(record.tanggal), "%Y-%m-%d").strftime('%B')
            else:
                record.bulan = "ANJAS KELAS"

    @api.depends('tanggal')
    def _jumlah_selesai(self):
        for rec in self:
            rec.jumlah_data_selesai_per_bulan = self.env['jumlah.data'].search_count([('state', '=', 'selesai'), ('bulan', '=', rec.bulan)])
