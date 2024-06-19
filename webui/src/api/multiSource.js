import axiosReq from '@/utils/axios-req'


// 获取数据执行方案
export const multiSourceDataChatReq = (query) => {
  return axiosReq({
    url: 'multi_source_data/chat',
    data: {
      query,
    },
    type: 'chat',
    method: 'post',
    timeout: 300000
  })
}

// 运行代码
export const runCodeReq = (code, filePaths) => {
  return axiosReq({
    url: 'multi_source_data/run_code',
    data: {
      code,
      filePaths
    },
    method: 'post',
    reqLoading: false,
    timeout: 300000
  })
}

// 获取所有文件
export const allMultiSourceFilesReq = () => {
  return axiosReq({
    url: 'multi_source_data/all_files',
    method: 'get',
    reqLoading: true,
    timeout: 10000
  })
}

export const uploadMultiSourceFileReq = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return axiosReq({
    url: 'multi_source_data/upload_file',
    data: formData,
    method: 'post',
    cache: false,
    contentType: false,
    processData: false,
    timeout: 0,
  })
}
