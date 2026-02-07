import request from "@/utils/request";

const API_PATH = "/lab/calc";

const LabCalcAPI = {
  // 列表查询
  listLabCalc(query: LabCalcPageQuery) {
    return request<ApiResponse<PageResult<LabCalcTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailLabCalc(id: number) {
    return request<ApiResponse<LabCalcTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createLabCalc(body: LabCalcForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateLabCalc(id: number, body: LabCalcForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteLabCalc(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchLabCalc(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportLabCalc(query: LabCalcPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateLabCalc() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importLabCalc(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default LabCalcAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface LabCalcPageQuery extends PageQuery {
  name?: string;
  field?: string;
  category?: string;
  description?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface LabCalcTable extends BaseType {
  name?: string;
  field?: string;
  category?: string;
  image?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface LabCalcForm extends BaseFormType {
  name?: string;
  field?: string;
  category?: string;
  image?: string;
}
