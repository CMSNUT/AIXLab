import request from "@/utils/request";

const API_PATH = "/resource/paper";

const ResourcePaperAPI = {
  // 列表查询
  listResourcePaper(query: ResourcePaperPageQuery) {
    return request<ApiResponse<PageResult<ResourcePaperTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailResourcePaper(id: number) {
    return request<ApiResponse<ResourcePaperTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createResourcePaper(body: ResourcePaperForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateResourcePaper(id: number, body: ResourcePaperForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteResourcePaper(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchResourcePaper(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportResourcePaper(query: ResourcePaperPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateResourcePaper() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importResourcePaper(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default ResourcePaperAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface ResourcePaperPageQuery extends PageQuery {
  type?: string;
  field?: string;
  title?: string;
  source?: string;
  year?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  doi?: string;
  pmid?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface ResourcePaperTable extends BaseType {
  type?: string;
  field?: string;
  title?: string;
  source?: string;
  year?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  doi?: string;
  pmid?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface ResourcePaperForm extends BaseFormType {
  type?: string;
  field?: string;
  title?: string;
  source?: string;
  year?: string;
  volume?: string;
  issue?: string;
  pages?: string;
  doi?: string;
  pmid?: string;
}
