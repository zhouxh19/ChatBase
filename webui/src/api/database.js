import axiosReq from '@/utils/axios-req'


// 获取数据库DDL
export const dbDdlInfoReq = (config) => {
  return axiosReq({
    url: 'db/db_ddl_info',
    data: {
      host: config.host,
      port: config.port,
      password: config.password,
      user: config.user,
      database: config.database
    },
    method: 'post',
    timeout: 10000
  })
}

// 生成sql语句
export const dbGenerateSqlReq = (query, ddl, modelName) => {
  return axiosReq({
    url: 'db/db_generate_sql',
    data: {query, ddl, model_name: modelName},
    method: 'post',
    type: 'chat',
    reqLoading: false,
    timeout: 10000
  })
}

export const dbExecuteSqlReq = (sql, host, user, password, database, port) => {
  return axiosReq({
    url: 'db/db_execute_sql',
    data: {host, user, password, database, port, sql},
    method: 'post',
    reqLoading: false,
    timeout: 20000
  })
}
