import json

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPBadRequest,
)

from ..models import Matakuliah


@view_config(route_name='matakuliah_list', renderer='json')
def matakuliah_list(request):
    """GET /api/matakuliah -> ambil semua matakuliah"""
    dbsession = request.dbsession
    mks = dbsession.query(Matakuliah).all()
    return {'matakuliah': [mk.to_dict() for mk in mks]}


@view_config(route_name='matakuliah_detail', renderer='json')
def matakuliah_detail(request):
    """GET /api/matakuliah/{id} -> detail satu matakuliah"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']

    mk = dbsession.query(Matakuliah).filter_by(id=mk_id).first()
    if mk is None:
        return HTTPNotFound(json_body={'error': 'Matakuliah tidak ditemukan'})

    return {'matakuliah': mk.to_dict()}


@view_config(route_name='matakuliah_add', request_method='POST', renderer='json')
def matakuliah_add(request):
    """POST /api/matakuliah -> tambah matakuliah baru"""
    try:
        data = request.json_body
    except json.JSONDecodeError:
        return HTTPBadRequest(json_body={'error': 'Body harus JSON'})

    # Validasi field wajib
    required = ['kode_mk', 'nama_mk', 'sks', 'semester']
    for field in required:
        if field not in data:
            return HTTPBadRequest(json_body={'error': f'Field {field} wajib diisi'})

    try:
        mk = Matakuliah(
            kode_mk=data['kode_mk'],
            nama_mk=data['nama_mk'],
            sks=int(data['sks']),
            semester=int(data['semester']),
        )

        dbsession = request.dbsession
        dbsession.add(mk)
        dbsession.flush()  # supaya mk.id terisi

        return {'success': True, 'matakuliah': mk.to_dict()}
    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})


@view_config(route_name='matakuliah_update', request_method='PUT', renderer='json')
def matakuliah_update(request):
    """PUT /api/matakuliah/{id} -> update matakuliah"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']

    mk = dbsession.query(Matakuliah).filter_by(id=mk_id).first()
    if mk is None:
        return HTTPNotFound(json_body={'error': 'Matakuliah tidak ditemukan'})

    try:
        data = request.json_body
    except json.JSONDecodeError:
        return HTTPBadRequest(json_body={'error': 'Body harus JSON'})

    # Update hanya field yang dikirim
    if 'kode_mk' in data:
        mk.kode_mk = data['kode_mk']
    if 'nama_mk' in data:
        mk.nama_mk = data['nama_mk']
    if 'sks' in data:
        mk.sks = int(data['sks'])
    if 'semester' in data:
        mk.semester = int(data['semester'])

    return {'success': True, 'matakuliah': mk.to_dict()}


@view_config(route_name='matakuliah_delete', request_method='DELETE', renderer='json')
def matakuliah_delete(request):
    """DELETE /api/matakuliah/{id} -> hapus matakuliah"""
    dbsession = request.dbsession
    mk_id = request.matchdict['id']

    mk = dbsession.query(Matakuliah).filter_by(id=mk_id).first()
    if mk is None:
        return HTTPNotFound(json_body={'error': 'Matakuliah tidak ditemukan'})

    dbsession.delete(mk)

    return {
        'success': True,
        'message': f'Matakuliah dengan id {mk_id} berhasil dihapus'
    }
