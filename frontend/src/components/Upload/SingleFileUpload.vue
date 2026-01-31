<!-- 单文件上传组件（支持拖拽+点击上传） -->
<template>
  <div class="single-file-upload">
    <el-upload
      v-model:file-list="internalFileList"
      class="single-upload"
      list-type="text"
      :show-file-list="false"
      :accept="props.accept"
      :before-upload="handleBeforeUpload"
      :http-request="handleUpload"
      :on-success="onSuccess"
      :on-error="onError"
      :on-remove="handleDelete"
      :disabled="props.disabled"
      :drag="true" 
    >
      <template #default>
        <!-- 拖拽/点击上传区域 -->
        <div class="single-upload__upload-area" :style="props.style">
          <!-- 已上传文件展示 -->
          <template v-if="internalFileList && internalFileList.length > 0 && internalFileList[0].url">
            <div class="single-upload__file-info">
              <el-icon class="single-upload__file-icon"><Document /></el-icon>
              <div class="single-upload__file-detail">
                <p class="single-upload__file-name" :title="internalFileList[0].name">
                  {{ internalFileList[0].name }}
                </p>
                <p class="single-upload__file-size">
                  {{ formatFileSize(internalFileList[0].size || 0) }}
                </p>
              </div>
              <!-- 删除按钮 -->
              <el-icon
                v-if="!props.disabled"
                class="single-upload__delete-btn"
                @click.stop="handleDelete"
              >
                <CircleCloseFilled />
              </el-icon>
            </div>
          </template>
          <!-- 未上传文件展示（拖拽/点击提示） -->
          <template v-else>
            <el-icon class="single-upload__add-icon"><Upload /></el-icon>
            <p class="single-upload__upload-tip">点击或拖拽文件到此处上传</p>
            <p class="single-upload__format-tip">支持 {{ props.accept || "所有" }} 格式，最大 {{ props.maxFileSize }}MB</p>
          </template>
        </div>
      </template>
    </el-upload>
    <!-- 额外提示文本 -->
    <div v-if="props.showTip" class="el-upload__tip">
      {{ props.tipText || `支持 ${props.accept || "所有"} 格式，文件大小不超过 ${props.maxFileSize}MB` }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { UploadRawFile, UploadRequestOptions, ElMessage, type UploadUserFile } from "element-plus";
import { Document, Upload, CircleCloseFilled } from "@element-plus/icons-vue";
import ParamsAPI from "@/api/module_system/params";

// 定义文件路径类型（与原组件保持一致）
type UploadFilePath = {
  file_name: string;
  file_url: string;
  [key: string]: any;
};

const props = defineProps({
  /**
   * 请求携带的额外参数
   */
  data: {
    type: Object,
    default: () => {
      return {};
    },
  },
  /**
   * 上传文件的参数名
   */
  name: {
    type: String,
    default: "file",
  },
  /**
   * 最大文件大小（单位：M）
   */
  maxFileSize: {
    type: Number,
    default: 200,
  },
  /**
   * 上传文件格式，默认支持所有文件（空字符串），指定格式示例：'.pdf,.doc,.docx,.zip'
   */
  accept: {
    type: String,
    default: "", // 核心修改：默认支持所有文件
  },
  /**
   * 自定义样式，用于设置上传区域的宽度和高度等其他样式
   */
  style: {
    type: Object,
    default: () => {
      return {
        width: "300px",
        height: "180px",
        border: "1px dashed #dcdfe6",
      };
    },
  },
  /**
   * 是否禁用
   */
  disabled: {
    type: Boolean,
    default: false,
  },
  /**
   * 是否显示提示信息
   */
  showTip: {
    type: Boolean,
    default: false,
  },
  /**
   * 提示文本
   */
  tipText: {
    type: String,
    default: "",
  },
});

// 接收字符串类型的modelValue，绑定文件URL，与原组件保持兼容
const modelValue = defineModel<string>({
  default: "",
});

// 内部使用的文件列表
const internalFileList = ref<UploadUserFile[]>([]);

// 监听modelValue变化，同步到internalFileList
watch(
  () => modelValue.value,
  (newVal) => {
    if (newVal) {
      internalFileList.value = [
        {
          name: newVal.split("/").pop() || "file",
          url: newVal,
          size: 0, // 文件大小默认0，若后端返回可补充
        },
      ];
    } else {
      internalFileList.value = [];
    }
  },
  { immediate: true }
);

// 监听internalFileList变化，同步到modelValue
watch(
  () => internalFileList.value,
  (newVal) => {
    if (newVal && newVal.length > 0 && newVal[0].url) {
      modelValue.value = newVal[0].url;
    } else {
      modelValue.value = "";
    }
  },
  { deep: true }
);

/**
 * 定义组件触发的事件
 */
const emit = defineEmits<{
  (e: "success", fileInfo: UploadFilePath): void;
  (e: "error", error: any): void;
  (e: "input", value: string): void;
  (e: "update:modelValue", value: string): void;
}>();

/**
 * 格式化文件大小（字节转友好显示）
 */
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
};

/**
 * 限制用户上传文件的格式和大小（复用原逻辑，适配文件场景）
 */
function handleBeforeUpload(file: UploadRawFile) {
  // 若未限制格式，直接通过格式校验
  if (!props.accept) return true;

  const acceptTypes = props.accept.split(",").map((type) => type.trim());

  // 检查文件格式是否符合 accept
  const isValidType = acceptTypes.some((type) => {
    if (type.startsWith(".")) {
      // 扩展名校验（.pdf, .doc）
      return file.name.toLowerCase().endsWith(type.toLowerCase());
    } else if (type.includes("/")) {
      // MIME 类型校验（application/pdf）
      return file.type === type;
    } else {
      // 兼容特殊场景，默认通过
      return true;
    }
  });

  if (!isValidType) {
    ElMessage.warning(`上传文件的格式不正确，仅支持：${props.accept}`);
    return false;
  }

  // 限制文件大小
  if (file.size > props.maxFileSize * 1024 * 1024) {
    ElMessage.warning(`上传文件不能大于 ${props.maxFileSize}MB`);
    return false;
  }

  // 缓存文件大小到内部列表，用于展示
  internalFileList.value = [{ name: file.name, size: file.size, url: "" }];
  return true;
}

/**
 * 上传文件（完全复用原组件逻辑，无修改）
 */
async function handleUpload(options: UploadRequestOptions) {
  try {
    const file = options.file;
    const formData = new FormData();

    formData.append(props.name, file);

    // 处理附加参数
    for (const [key, value] of Object.entries(props.data)) {
      formData.append(key, String(value));
    }

    const response = await ParamsAPI.uploadFile(formData);

    if (response.data.code === 0 && response.data) {
      const fileInfo: UploadFilePath = response.data.data;
      onSuccess(fileInfo);
      return fileInfo;
    } else {
      const errorMsg = response.data.msg || "上传失败";
      ElMessage.error(errorMsg);
      throw new Error(errorMsg);
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
    throw error;
  }
}

/**
 * 删除文件（复用原组件逻辑）
 */
function handleDelete() {
  internalFileList.value = [];
  ElMessage.success("文件已删除");
}

/**
 * 上传成功回调（适配文件信息展示）
 */
const onSuccess = (fileInfo: UploadFilePath) => {
  // 更新绑定的值为文件URL，缓存文件名和大小
  const newFileList = [
    {
      name: fileInfo.file_name,
      url: fileInfo.file_url,
      size: internalFileList.value[0]?.size || 0,
    },
  ];

  internalFileList.value = newFileList;

  // 触发事件
  emit("success", fileInfo);
  emit("input", fileInfo.file_url);
  emit("update:modelValue", fileInfo.file_url);
  ElMessage.success("文件上传成功");
};

/**
 * 上传失败回调（复用原组件逻辑）
 */
const onError = (error: any) => {
  console.error("文件上传失败:", error);
  ElMessage.error("文件上传失败，请重试");
  internalFileList.value = [];
  emit("error", error);
};
</script>

<style scoped lang="scss">
.single-file-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.single-upload {
  &__upload-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    background-color: #fafbfc;
    cursor: pointer;
    transition: all 0.3s ease;

    // 拖拽悬浮/选中样式（el-upload自带drag类）
    :deep(.el-upload-dragger:hover &) {
      border-color: #409eff;
      background-color: #f0f7ff;
    }

    :deep(.el-upload-dragger.is-dragover &) {
      border-color: #409eff;
      background-color: #f0f7ff;
    }
  }

  &__file-info {
    display: flex;
    align-items: center;
    width: 100%;
    height: 100%;
    padding: 0 20px;
  }

  &__file-icon {
    font-size: 24px;
    color: #409eff;
    margin-right: 16px;
  }

  &__file-detail {
    flex: 1;
    overflow: hidden;
  }

  &__file-name {
    margin: 0 0 4px 0;
    font-size: 14px;
    color: #303133;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  &__file-size {
    margin: 0;
    font-size: 12px;
    color: #909399;
  }

  &__delete-btn {
    font-size: 18px;
    color: #f56c6c;
    cursor: pointer;
    transition: color 0.3s ease;

    &:hover {
      color: #e4393c;
    }
  }

  &__add-icon {
    font-size: 36px;
    color: #c0c4cc;
    margin-bottom: 12px;
  }

  &__upload-tip {
    font-size: 14px;
    color: #303133;
    margin: 0 0 4px 0;
  }

  &__format-tip {
    font-size: 12px;
    color: #909399;
    margin: 0;
  }
}

.el-upload__tip {
  margin-top: 7px;
  font-size: 12px;
  color: #606266;
}
</style>