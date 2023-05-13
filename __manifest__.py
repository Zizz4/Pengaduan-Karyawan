{
    'name': 'Pengaduan Karyawan',
    'version': '1.0',
    'sequence': 1,
    'summary': 'Aplikasi untuk melakukan pengaduan',
    'description': 'Dengan Aplikasi ini, para karyawan dapat melakukan pengaduan terhadap apapun kepada atasannya.',
    'category': 'Productivity',
    'author': 'Muhamad Syahril Aziz',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/role.xml',
        'security/ir.model.access.csv',
        'views/admin.xml',
        'views/pengaduan.xml',
        'views/pengaduan_admin.xml',
        'views/tanggapan.xml',
        'views/masyarakat.xml',
        'report/laporan.xml',
        'report/laporan2.xml'
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}
