import request from '@/utils/request'

const api_root = '/sxcapi-dtm/DutyPersonnel/'

export function getList(params, child = '') {
  return request({
    url: api_root + child, // child末尾自带有 / 结尾
    method: 'get',
    params: params
  })
}

export function create(data) {
  return request({
    url: api_root,
    method: 'post',
    data: data
  })
}

export function update(id, data) {
  return request({
    url: api_root + id + '/',
    method: 'patch',
    data: data
  })
}

export function remove(id) {
  return request({
    url: api_root + id + '/',
    method: 'delete'
  })
}

export function batchUpdate(data) {
  return request({
    url: api_root,
    method: 'patch',
    data: data
  })
}

export function batchDelete(id_list) {
  return request({
    url: api_root,
    method: 'delete',
    data: id_list
  })
}
